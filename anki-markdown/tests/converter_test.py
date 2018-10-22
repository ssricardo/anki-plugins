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
<div>```</div><div>&nbsp; &nbsp; &nbsp; &nbsp; System.out.println();</div><div>&nbsp; &nbsp; &nbsp; &nbsp; def test():</div><div>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ra()</div><div>```</div>
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

MD_WITH_CODE = """
* La casa del papel

> Um seriado espanol

```
    System.out.println();
          def test():
              code()
```  
  

"""

class TransformerTest(unittest.TestCase):

    tested = Converter()

    def setUp(self):
        print('---------------------------------------')
        

    @unittest.skip
    def testExecution(self):
        res = self.tested.convertMarkdown(MD_1)
        self.assertIsNotNone(res)
        print(res)

    # @unittest.skip
    def testCodeFormat(self):
        res = self.tested.convertMarkdown(MD_WITH_CODE)
        self.assertIsNotNone(res)
        print(res)

    @unittest.skip
    def testTransformArea(self):
        value = self.tested.findConvertArea(MD_DELIMITED)
        self.assertIsNotNone(value)
        print(value)

    @unittest.skip
    def testClearHTML(self):
        value = self.tested.getTextFromHtml(HTML_CODE)
        self.assertIsNotNone(value)
        print(value)

    # @unittest.skip
    def testCodeHTML2(self):
        value = self.tested.findConvertArea(HTML_CODE2)
        print(value)

    # @unittest.skip
    def testCodeHTML3(self):
        value = self.tested.findConvertArea(HTML_CODE3)
        print(value)

    @unittest.skip
    def testMultipleBlocks(self):
        value = self.tested.findConvertArea(MULTIPLE_BLOCKS)
        print(value)

unittest.main()