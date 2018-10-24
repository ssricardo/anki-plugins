# -*- coding: utf-8 -*-
# Related to converter

# This files is part of anki-markdown addon
# @author ricardo saturnino
# ------------------------------------------------

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import unittest
from anki_markdown.converter import Converter

MD_1 = """
# Header 1

* My list item
* Item 2

> My quote
"""

MD_CODE = """
# My code
    
:::python  
    def myPythonCode(self):
        testCodeFormat()


In line code `private void method(String v)`
"""

MD_DELIMITED = """
<i>Outer MD</i>
<amd>
# Converted
    
* Inside MD area

> Done!
</amd>

<div>After MD</div>
"""

HTML_CODE = """
<div>My code</div>
    
&gt; Some text here    

    Some code &amp;&amp; other simbol &lt; all
"""

HTML_CODE2 = """
<amd>
	## Exemplos vão aqui!<div><br></div><div>* La casa del papel</div><div><br></div><div>&gt; Um seriado espanol</div>
<div><br></div><div>```print()```</div>
	</amd>
"""

HTML_CODE3 = """
<amd>
<div>&nbsp; &nbsp; &nbsp; &nbsp; System.out.println();</div><div>&nbsp; &nbsp; &nbsp; &nbsp; def test():</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ra()</div>
	</amd>
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

MULTIPLE_BLOCKS = """
<amd>
    <amd>       ## Header 2</amd>
Some text <br>
<div>Something</div>
</amd>

Other text
<amd>       ### Header 3</amd>
"""

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

    def testTransformArea(self):
        value = self.tested.findConvertArea(MD_DELIMITED, True, False)
        self.assertIsNotNone(value)
        self.assertTrue("""<i>Outer MD</i>
<h1>Converted</h1>
<ul>""" in value)
        self.assertFalse('<amd>' in value)

    def testClearHTML(self):
        value = self.tested.getTextFromHtml(HTML_CODE, False)        
        self.assertIsNotNone(value)
        self.assertTrue("> Some text here" in value)
        self.assertFalse("&gt;" in value)

    def testCodeHTML2(self):
        value = self.tested.findConvertArea(HTML_CODE2, True, False)
        self.assertTrue("<h2>Exemplos vão aqui!</h2>" in value)
        self.assertTrue("<code>" in value)

        value = self.tested.findConvertArea(HTML_CODE2, False, False)   # no strip
        self.assertFalse("<h2>Exemplos vão aqui!</h2>" in value)    # line beggining may fail

    def testCodeHTML3(self):
        value = self.tested.findConvertArea(HTML_CODE3, True, False)
        self.assertFalse("<code>" in value)

        value = self.tested.findConvertArea(HTML_CODE3, False, True) # no strip, replace &nbsp;
        self.assertTrue("<code>" in value)
        # print(value)

    def testInlineTrimParam(self):
        res = self.tested.findConvertArea("""<amd trim="true">  <i>  # Header</i>  </amd>""", False, False)
        self.assertTrue('<h1>Header' in res)
        self.assertFalse('  # Header' in res)

    def testInlineReplaceSpace(self):
        res = self.tested.findConvertArea("""<amd replace-spaces="true">  *&nbsp;ListItem&nbsp;  </amd>""", True, False)
        self.assertTrue('<li>ListItem' in res)
        self.assertFalse('  *List' in res)

    # HTML with inline options
    def testComplete(self):
        res = self.tested.findConvertArea("""
<amd trim="false" replace-spaces="true">
    <div>&nbsp; &nbsp; &nbsp; &nbsp; System.out.println();</div><div>&nbsp; &nbsp; &nbsp; &nbsp; def test():</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ra()</div>
</amd>""", True, False)
        self.assertTrue('<code>' in res)


    @unittest.skip
    def testMultipleBlocks(self):
        value = self.tested.findConvertArea(MULTIPLE_BLOCKS, True, False)
        print(value)

unittest.main()