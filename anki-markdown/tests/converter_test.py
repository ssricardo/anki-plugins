# -*- coding: utf-8 -*-
# Related to converter

# This files is part of anki-markdown addon
# @author ricardo saturnino
# ------------------------------------------------

import sys
import os
from re import Pattern

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../src')

from converter import Converter

# region Markdowns

MD_1 = """
# Header 1

* My list item
* Item 2

> My quote
"""

MD_WITH_CODE = """
* La casa del papel

> Um seriado espanol

```
    System.out.println();
          def test():
              code()
```  
  
"""

# endregion

# region HTMLs

HTML_CODE1 = """
    <h1>Header 1</h1>

    <ul>
        <li>My list item</li>
        <li>Item 2</li>
    </ul>

    <blockquote>My quote</blockquote>
"""

HTML_CODE2 = """
<div>My code</div>
    
&gt; Some text here    

    Some code &amp;&amp; other simbol &lt; all
"""

# endregion

# region DELIMITED CODES

MD_DELIMITED = """
<i>Outer MD</i>
<amd>
# Converted
    
* Inside MD area

> Done!
</amd>

<div>After MD</div>
"""

DEMILITED_CODE = """
<amd>
## Exemplos vão aqui!  
<div><br></div><div>* La casa del papel</div><div><br></div><div>&gt; Um seriado espanol</div>
    <div><br></div><div>```print()```</div>
	</amd>
"""

DEMILITED_CODE2 = """
<amd>
<div>&nbsp; &nbsp; &nbsp; &nbsp; System.out.println();</div><div>&nbsp; &nbsp; &nbsp; &nbsp; def test():</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ra()</div>
	</amd>
"""

MULTIPLE_BLOCKS = """
<amd>
    <amd>       ## Header 2</amd>
Some text <br>
<div>Something</div>
</amd>

Other text
<amd>       ### Header 3</amd>
"""

BLOCK_CLOZE = """
<amd>
# Code with cloze
    
    :::python
    def <span class=cloze>[...]</span>: 
    def <span class=cloze>Result</span> area
    def <span class=cloze>[...]</span>: 
    

> Done!
</amd>
"""

BLOCK_INPUTS = """
<amd>
# Code with inputs, for type
    
    def <input type=text style="anytrhing;" />: 
    def <input id="iptID" type="text" style="anytrhing;" onclick="function()"> area
    def <span class=cloze>[...]</span>: 

> Done!
</amd>
"""

# endregion

tested: Converter = Converter()


def setUp():
    # print('---')
    pass


def test_ConversionMD():
    res: str = tested.convertMarkdown(MD_1)
    assert (res is not None)
    assert ('<h1>Header' in res)
    assert ('<li>Item' in res)
    assert ('* Item' not in res)


def test_CodeFormat():
    res = tested.convertMarkdown(MD_WITH_CODE)
    assert (res is not None)
    assert ('<code>System.out.println();' in res)
    assert ("""<blockquote>\n<p>Um""" in res)


def test_TransformArea():
    value: str = tested.convertAmdAreasToMD(MD_DELIMITED)
    value = value.replace('\n', '')
    assert (value is not None)
    assert ("""<i>Outer MD</i><span class="amd"><h1>Converted</h1><ul><li>Inside MD area</li></ul><blockquote><p>Done!</p></blockquote></span><div>After MD</div>"""
            in value)
    assert ('<amd>' not in value)


def test_ClearHTML():
    value = tested.getTextFromHtml(HTML_CODE2)
    assert (value is not None)
    assert ("> Some text here" in value)
    assert ("&gt;" not in value)


def test_TextWithHTML():
    # cleanedCode = tested.getTextFromHtml(DEMILITED_CODE.strip())
    value = tested.convertAmdAreasToMD(DEMILITED_CODE, True)
    assert ("<h2>Exemplos vão aqui!</h2>" in value)
    assert ("<code>" in value)


def testTextWithHTML2():
    value = tested.convertAmdAreasToMD(DEMILITED_CODE2, True)
    assert ("<code>" in value)


# TODO re check cases with spaces
def testInlineTrimParam():
    res = tested.convertAmdAreasToMD("""<amd trim="true">  <i>  # Header</i>  </amd>""")
    assert ('<h1>Header' in res)
    assert ('  # Header' not in res)


# HTML with inline options
def testConvertArea():
    res = tested.convertAmdAreasToMD("""
<amd trim="false" replace-spaces="true">
      System.out.println();\\n    def test():\\n
      ra()
</amd>""")
    print(res)
    assert ('<code>' in res)


def test_ClozeParts():
    res = tested.convertAmdAreasToMD(BLOCK_CLOZE)
    # print(res)
    assert ('def <span class=cloze>[...]' in res)
    assert ('def <span class=cloze>Result' in res)
    assert ('[[...CLOZE...]]' not in res)


def test_cloze_regex():
    rg: Pattern = tested._clozeRE
    res = rg.search('<span class=cloze>Result</span> Something else')
    assert res is not None
    assert res.group(1) == 'Result'

    res = rg.search('<span class="cloze md-test">Result</span> Something else')
    assert res is not None
    assert res.group(1) == 'Result'


def test_preProcessContent():
    content = """
    
        LocalDate localDate = LocalDate.of(2017, 07, 8);
        LocalDate nextSunday = localDate.with(<span class="cloze st-correct">TemporalAdjusters</span>.next(<span class=cloze>DayOfWeek</span>.SUNDAY)
    """
    result = tested._processContent(content, False, False)
    print(result)


def test_InputsParts():
    res = tested.convertAmdAreasToMD(BLOCK_INPUTS, isTypeMode=True)

    # print(res, flush=True)
    assert ('def <input type=text style="anytrhing;" />' in res)
    assert ('id="iptID"' in res)
    assert ('||...INPUT...||' not in res)


def test_fix_escaped_inputs():
    content = """
        <div>Puts the names of the male members in a <u>collection</u>:</div>
        <div><br /></div>
        <div><pre class="myCodeClass">List&lt;String&gt; namesOfMaleMembersCollect = roster
        &nbsp; &nbsp; .stream()
        &nbsp; &nbsp; .filter(p -&gt; p.getGender() == Person.Sex.MALE)
        &nbsp; &nbsp; .map(p -&gt; p.getName())
        &nbsp; &nbsp; .<input type="hidden" id="ansval0" value="collect" /><input type="text" id="typeans0" placeholder="" 
             onkeyup="checkFieldValue($('#ansval0').val(), 0);"
             class="ftb" style="width: 4.34em" />(<input type="hidden" id="ansval1" value="Collectors.toList()" /><input type="text" id="typeans1" placeholder="" 
             onkeyup="checkFieldValue($('#ansval1').val(), 1);"
             class="ftb" style="width: 11.78em" />);</pre></div>
        <pre><code>        &lt;input type="hidden" id="ansval" value="" /&gt;
        </code></pre>
    """
    result = tested._fix_escaped_inputs(content)
    assert '<input type="hidden" id="ansval" value="" />' in result

def testMultipleBlocks():
    value = tested.convertAmdAreasToMD(MULTIPLE_BLOCKS)
    print(value)


def testCodeToMarkdown():
    t = tested
    # print(t.getTextFromHtml(t.convertMarkdown("""
    # def _wrapOnPaste(self, fn):
    #     ref = self

    # def _onPaste(self, mode):
    #     extended = editor.mw.app.queryKeyboardModifiers() & Qt.ShiftModifier
    #     mime = editor.mw.app.clipboard().mimeData(mode=mode)
    # """)))


def test_stripAmdTags():
    t = tested
    assert ('{{FieldOne}}' == t.stripAmdTagForField('<amd>{{FieldOne}}</amd>', 'FieldOne'))
    assert ('{{FieldOne}}' == t.stripAmdTagForField('<amd some="param">{{FieldOne}}</amd>', 'FieldOne'))
    # assertEqual('More Content [[FieldOne]] After', t.stripAmdTags('More Content <amd>[[FieldOne]]</amd> After'))


def test_stripAmdTagsMultiple():
    t = tested
    assert('{{FieldOne}}' == t.stripAmdTagForField('<amd><amd>{{FieldOne}}</amd></amd>', 'FieldOne'))
    assert ('{{FieldOne}}<amd>:Two</amd>' ==
            t.stripAmdTagForField('<amd some="param">{{FieldOne}}</amd><amd>:Two</amd>', 'FieldOne'))

def test_table():
    from markdown import markdown

    res = markdown("""
nome | outro
---- | ----
value | va
    """, extensions=['tables', 'codehilite'])
    print(res)

def test_code():
    from markdown import markdown

    res = markdown("""
        def some_py_fun(self):
          a = self.test()
          print(a)
    """, extensions=['codehilite'])
    print(res)
