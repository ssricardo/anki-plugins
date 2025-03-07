import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../src')

from handler import FieldsContext, AnkiInterface, addon_field_filter, handle_answer, _format_field_result
from anki_mocks_test import TestReviewer, TestCard

AnkiInterface.strip_HTML = lambda i: i

class FilterContext:

    def __init__(self, c_ord: int):
        self._card = TestCard()
        self._card.ord = c_ord - 1

    def card(self):
        return self._card


def test_other_filter():
    data = """This is a <span class="cloze" 
     data-ordinal="1">test</span"""
    res = addon_field_filter(data, "Text", "other-filter", FilterContext(1))

    assert res == data


def test_filter():
    data = """
        This is a <span class="cloze-inactive" 
     data-ordinal="1">test</span>&nbsp;<br>With some toher <span class="cloze" 
     data-cloze="fields" data-ordinal="2">[...]</span>.<br>And two fields on the  
     <span class="cloze-inactive" data-ordinal="1">same</span><br><br>But not  
     type.<br>And field with <span class="cloze-inactive"  
     data-ordinal="3">double</span> field upd field upd 
    """

    res = addon_field_filter(data, "Text", "fill-blanks", FilterContext(2))

    print(res)
    assert 'id="ansval0" type="hidden" value="fields"' in res
    assert 'typeans0' in res


def test_filter2():
    data = """
This is a <span class="cloze-inactive" data-ordinal="1">test</span>&nbsp;<br>With some toher <span class="cloze" data-ordinal="2">fields</span>.<br>And two fields on the <span class="cloze-inactive" data-ordinal="1">same</span><br><
br>But not type.<br>And field with <span class="cloze-inactive" data-ordinal="3">double</span> field upd field upd
    """

    res = addon_field_filter(data, "Text", "fill-blanks", FilterContext(2))

    print(res)


def test_multiple():
    data = """
This is a <span class="cloze" data-ordinal="1">test</span>&nbsp;<br>With some toher <span class="cloze-inactive" data-ordinal="2">fields</span>.
<br>And two fields on the <span class="cloze" data-ordinal="1">same</span><br><br>But not type.
<br>And field with <span class="cloze-inactive" data-ordinal="3">double</span> field upd field upd
    """

    res = addon_field_filter(data, "Text", "fill-blanks", FilterContext(1))

    assert 'id="ansval0" type="hidden" value="test"' in res
    assert 'id="ansval1" type="hidden" value="same"' in res
    assert 'ansval2' not in res


def test_filter_with_hint():
    data = """This is a <span class="cloze-inactive" data-ordinal="1">test</span>&nbsp;<br>With some toher <span class="cloze-inactive" data-ordinal="2">fields</span>.<br>And two fields on the <span class="cloze-inactive" data-ordinal="1">same</s
pan><br><br>But not type.<br>And field with <span class="cloze" data-cloze="double" data-ordinal="3">[comma]</span> hint
    """

    res = addon_field_filter(data, "Text", "fill-blanks", FilterContext(3))

    assert 'value="double"' in res
    assert 'placeholder="comma"' in res


def test_answer_correct():
    content = """
<style>.card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}
.cloze {
    font-weight: bold;
    color: blue;
}
.nightMode .cloze {
    color: lightblue;
}
</style>This is a <span class="cloze-inactive" data-ordinal="1">test</span>&nbsp;<br>With some toher <span class="cloze-inactive" data-ordinal="2">fields</span>.<br>And two fields on the <span class="cloze-inactive" data-ordinal="1"
>same</span><br><br>But not type.<br>And field with <span class="cloze" data-ordinal="3">double</span> hint
<br>
A value in the back field upd field upd

    """

    FieldsContext.entry_number = 1
    FieldsContext.answers = ["double"]
    res = handle_answer(content, TestCard(), "reviewAnswer")

    assert '<span class="cloze st-ok">double</span>' in res

def test_answer_wrong():
    content = """
<style>.card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}
.cloze {
    font-weight: bold;
    color: blue;
}
.nightMode .cloze {
    color: lightblue;
}
</style>This is a <span class="cloze-inactive" data-ordinal="1">test</span>&nbsp;<br>With some toher <span class="cloze-inactive" data-ordinal="2">fields</span>.<br>And two fields on the <span class="cloze-inactive" data-ordinal="1"
>same</span><br><br>But not type.<br>And field with <span class="cloze" data-ordinal="3">double</span> hint
<br>
A value in the back field upd field upd
    """

    FieldsContext.entry_number = 1
    FieldsContext.answers = ["something-else"]
    res = handle_answer(content, TestCard(), "reviewAnswer")

    assert "st-expected" in res
    assert "st-error" in res

# --------------------------------- From previous version - tests --------------------------------------------

def test_nocloze():
    data = """
    <span class="cloze-inactive" data-cloze="fields" data-ordinal="2">
        Single value
        Multiline
     </span>
    """

    res = addon_field_filter(data, "Text", "fill-blanks", FilterContext(2))

    assert ('Single value' in res)
    assert 'ansval0' not in res


def test_with_quotes():
    data = """
        A small step for a man, <br>a big 
        <span class="cloze" data-cloze="one&#x28;&quot;q&quot;&#x2C;&#x20;&#x27;step&#x27;&#x29;" data-ordinal="1">[...]</span>, 
        <span class="cloze" data-cloze="&#x2E;&#x2E;" data-ordinal="1">[...]</span>..
.<br> <span class="cloze-inactive" data-ordinal="2">plainText</span>
        """

    res = addon_field_filter(data, "Text", "fill-blanks", FilterContext(1))

    print(res)

    assert """<input id="ansval0" type="hidden" value="one(&quot;q&quot;, 'step')"/>""" in res


def test_withRegexStr():
    data = """
        Some content here <span class="cloze" data-cloze="with&#x20;&#x5B;&#x20;&#x5C;&#x5C;t&#x5C;&#x5C;n&#x5C;&#x5C;x&#x5C;&#x5C;r&#x5C;&#x5C;f&#x5D;" data-ordinal="1">[...]</span>
    """

    res = addon_field_filter(data, "Text", "fill-blanks", FilterContext(1))

    print(res)

    assert """\\\\t\\\\n\\\\x\\\\r\\\\f""" in res


def test_field_result_uppercase_error():
    result = _format_field_result('milano', 'Milano')
    assert 'st-error' in str(result)


def test_field_result_ignore_case():
    FieldsContext.ignore_case = True
    result = _format_field_result('milano', 'Milano')
    assert 'st-error' not in str(result)
    assert 'st-ok' in str(result)


def test_multiple_with_hint():
    data = """
Probleme mit der Sprache -&gt;&gt; <span class="cloze" data-cloze="Probleme" data-ordinal="1">[Pro...]</span> <span class="cloze-inactive" data-ordinal="2">mit</span> <span class="cloze" data-cloze="der" data-ordinal="1">[de...]</sp
an> <span class="cloze-inactive" data-ordinal="2">Sprache</span> After
    """

    res = addon_field_filter(data, "Text", "fill-blanks", FilterContext(1))

    print(res)
    assert ('typeans0' in res)
    assert 'placeholder="Pro..."' in res
    assert ('mit' in res)
