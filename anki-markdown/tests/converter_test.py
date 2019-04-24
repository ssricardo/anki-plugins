# -*- coding: utf-8 -*-
# Related to converter

# This files is part of anki-markdown addon
# @author ricardo saturnino
# ------------------------------------------------

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import unittest
from src.converter import Converter

#region Markdowns

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

#endregion

#region HTMLs

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

#endregion

#region DELIMITED CODES

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
	## Exemplos vão aqui!<div><br></div><div>* La casa del papel</div><div><br></div><div>&gt; Um seriado espanol</div>
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


#endregion

class TransformerTest(unittest.TestCase):

    tested = Converter()

    def setUp(self):
        # print('---')
        pass
        

    def testConversionMD(self):
        res:str = self.tested.convertMarkdown(MD_1)
        self.assertIsNotNone(res)
        self.assertTrue('<h1>Header' in res)
        self.assertTrue('<li>Item' in res)
        self.assertFalse('* Item' in res)

    def testCodeFormat(self):
        res = self.tested.convertMarkdown(MD_WITH_CODE)
        self.assertIsNotNone(res)
        self.assertTrue('<code>System.out.println();' in res)
        self.assertTrue("""<blockquote>\n<p>Um""" in res)

    # TODO re check cases with \n
    @unittest.skip
    def testTransformArea(self):
        value = self.tested.convertAmdAreasToMD(MD_DELIMITED)
        self.assertIsNotNone(value)
        self.assertTrue("""<i>Outer MD</i>
<h1>Converted</h1>
<ul>""" in value)
        self.assertFalse('<amd>' in value)

    def testClearHTML(self):
        value = self.tested.getTextFromHtml(HTML_CODE2)
        self.assertIsNotNone(value)
        self.assertTrue("> Some text here" in value)
        self.assertFalse("&gt;" in value)

    def testHtmlToMarkdown(self):
        value = self.tested.getTextFromHtml(HTML_CODE1)
        self.assertIsNotNone(value)
        self.assertTrue('# Header 1' in value)
        self.assertTrue('* My list item' in value)
        self.assertTrue('> My quote' in value)
        

    def testTextWithHTML(self):
        # cleanedCode = self.tested.getTextFromHtml(DEMILITED_CODE.strip())
        value = self.tested.convertAmdAreasToMD(DEMILITED_CODE, True)
        self.assertTrue("<h2>Exemplos vão aqui!</h2>" in value)
        self.assertTrue("<code>" in value)

    def testTextWithHTML2(self):
        value = self.tested.convertAmdAreasToMD(DEMILITED_CODE2, True)
        self.assertTrue("<code>" in value)

    # TODO re check cases with spaces
    @unittest.skip
    def testInlineTrimParam(self):
        res = self.tested.findConvertArea("""<amd trim="true">  <i>  # Header</i>  </amd>""")
        self.assertTrue('<h1>Header' in res)
        self.assertFalse('  # Header' in res)

    # HTML with inline options
    def testConvertArea(self):
        res = self.tested.convertAmdAreasToMD("""
<amd trim="false" replace-spaces="true">
          System.out.println();\\n    def test():\\n
          ra()
</amd>""")
        self.assertTrue('<code>' in res)

    def testClozeParts(self):
        res = self.tested.convertAmdAreasToMD(BLOCK_CLOZE)
        self.assertTrue('def <span class=cloze>[...]' in res)
        self.assertTrue('def <span class=cloze>Result' in res)
        self.assertFalse('[[...CLOZE...]]' in res)


    def testInputsParts(self):
        res = self.tested.convertAmdAreasToMD(BLOCK_INPUTS, isTypeMode=True)

        print(res, flush=True)
        self.assertTrue('def <input type=text style="anytrhing;" />' in res)
        self.assertTrue('id="iptID"' in res)
        self.assertFalse('||...INPUT...||' in res)


    @unittest.skip
    def testMultipleBlocks(self):
        value = self.tested.convertAmdAreasToMD(MULTIPLE_BLOCKS)
        print(value)

unittest.main()