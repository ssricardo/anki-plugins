# -*- coding: utf-8 -*-
# Related to typein handler
# Test code for config modules

# This files is part of fill-the-blanks addon
# @author ricardo saturnino
# ------------------------------------------------

import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../src')

# import config as cc

from handler import TypeClozeHandler, FieldsContext, FieldState, AnkiInterface
from config import ConfigService
from anki_mocks_test import TestReviewer

def hookFakeFn(*args, **vargs):
    pass


def wrapFake(*args, **vargs):
    print("Returning original. Each func should be replaced directly")
    return args[0]

reviewer = TestReviewer()

ankiInterfaceMock = AnkiInterface()
ankiInterfaceMock.staticReviewer = TestReviewer
ankiInterfaceMock.strip_HTML = lambda v: v
ankiInterfaceMock.wrap = wrapFake
ankiInterfaceMock.addHook = hookFakeFn


tested = TypeClozeHandler(reviewer, ankiInterfaceMock)

reviewer.typeAnsQuestionFilter = lambda buf: tested.typeAnsQuestionFilter(buf, reviewer.typeAnsQuestionFilter)
reviewer.typeAnsAnswerFilter = lambda buf: tested.typeAnsAnswerFilter(buf, reviewer.typeAnsAnswerFilter)
reviewer._getTypedAnswer = lambda _old: tested._getTypedAnswer(reviewer.typeAnsQuestionFilter)


def test_nocloze():
    res = reviewer.typeAnsQuestionFilter("""
        <span class="content">
        Single value
        Multiline
        </span>
    """)

    assert ('Single value' in res)

def test_cloze_notype():
    res = reviewer.typeAnsQuestionFilter("""
        <span class="content">
        SELECT .., <span class=cloze>...</span>  Option.
        </span>
    """)

    # print(res)
    assert ('<span class=cloze>...</span>' in res)

def test_single_clozeType():
    reviewer.card.note()['Text'] = 'Meu valor {{c1::Alterado}} usando cloze '
    res = reviewer.typeAnsQuestionFilter("""
        <span class="content">
        [[type:cloze:Text]]
        </span>
    """)

    print(res)
    assert ('<input type="text"' in res)
    assert ('typeans0' in res)

def test_multiple_clozeType():
    reviewer.card.note()['Text'] = """A small {{c1::step}} for a man, 
    a big {{c10::one}}...
        {{c2::plainText}}
    """

    res = reviewer.typeAnsQuestionFilter("""
        <span class="content">
        [[type:cloze:Text]]
        </span>
    """)

    print(res)
    assert ('<input type="text"' in res)
    assert (' a big one...' in res)
    assert ('typeans1' not in res)
    assert ('c2::' not in res)

def test_with_quotes():
    reviewer.card.note()['Text'] = """A small step for a man, 
    a big {{c1::one("q", 'step')}}, {{c1::..}}...
        {{c2::plainText}}
    """

    res = reviewer.typeAnsQuestionFilter("""
        <span class="content">
        [[type:cloze:Text]]
        </span>
    """)

    print(res)

def test_withRegexStr():
    reviewer.card.note()['Text'] = """
        Some content here with [ \\t\\n\\x\\r\\f].
    """

    res = reviewer.typeAnsQuestionFilter("""
        <span class="content">
        [[type:cloze:Text]]
        </span>
    """)

    print(res)

def test_typeAnsAnswerFilter_noTypeCorrect():
    reviewer.typeAnsAnswerFilter("""
        <span class="content">
        [[type:cloze:Text]]
        </span>
    """)

def test_typeAnsAnswerFilter_Ok():
    reviewer.typeCorrect = FieldsContext("""
        <span class="content">
        [...]
        </span>
    """, [FieldState("Text", None, "Text")])
    reviewer.typeCorrect.answers = list("whatever")
    reviewer.typeAnsAnswerFilter("""
        <span class="content">
        [[type:cloze:Text]]
        </span>
    """)

def test_field_result_uppercase_error():
    result = tested.format_field_result('milano', 'Milano')
    assert ('st-error' in result)

def test_field_result_ignore_case():
    testInstance = TypeClozeHandler(reviewer, ankiInterfaceMock, True)
    result = testInstance.format_field_result('milano', 'Milano')
    assert ('st-error' not in result)
    assert ('st-ok' in result)

def test_html_space():
    reviewer.card.note()['Text'] = 'Meu valor {{c1::ValueWith&nbsp;}} com tags {{c1::<span class="bla">Other<br/>val <span>}} '
    res = reviewer.typeAnsQuestionFilter("""
        <span class="content">
        [[type:cloze:Text]]
        </span>
    """)

    print(''.join(map(lambda v: "'%s'" % v.value, reviewer.typeCorrect.entries)))
    # print(res)
    # assert ('<input type="text"' in res)
    # assert ('typeans0' in res)

# -------------------------------------------------- Reported issues ------------------------------------------------

# Issue 31
def test_multiple_with_hint():
    reviewer.card.note()['Text'] = \
    'Probleme mit der Sprache ->> {{c1::Probleme::Pro...}} {{c2::mit::mi...}} {{c1::der::de...}} {{c2::Sprache::Spr...}} After'

    res = reviewer.typeAnsQuestionFilter("""
        <span class="content">
        [[type:cloze:Text]]
        </span>
    """)

    print(res)
    assert ('typeans0' in res)
    assert ('mit::mi...' not in res)
    assert ('mit' in res)

# Issue 34
def test_issue_34():
    reviewer.card.note()['Text'] = \
    'Testing my field {{c1::repeated}} using cloze and type'

    res = reviewer.typeAnsQuestionFilter("""
        <div style='font-family: Microsoft YaHei; font-size: 14px;color: blue'>《{{《》}}》</div><br>
        <div style='font-family: Microsoft YaHei; font-size: 20px;'>[[cloze:question]]</div></dir><br>
        <div style='font-family: Microsoft YaHei; font-size: 20px;'>[[type:cloze:Text]]</div></dir><br>
    """)

    print(res)
    assert ('typeans0' in res)

# Issue 45
def test_issue_45():
    reviewer.card.note()['Text'] = """
    Testing my field {{c1::repeated}} using cloze and type
    [sound:rec1579903-59_5.mp3] more content"""

    res = reviewer.typeAnsQuestionFilter("""            
        <span class="content">
        [[type:cloze:Text]]
        </span>
    """)

    print(res)
    assert ('typeans0' in res)
    assert ('more content' in res)
    assert ('[sound:rec1579903-59_5.mp3]' not in res)


# Issue 100
def test_issue_100():
    content = """
    <b>{{c1::Lenguaje}}&nbsp;o&nbsp;{{c1::facultad verbal}}:&nbsp;</b><br><ul><li>{{c2::Sistema psicologico cognitivo universal}}
     responsable de {{c2::la comunicacian}}.</li><li>Es {{c2::una facultad}} del {{c2::ser humano}}.</li>
     <li>Es {{c2::biológicamente innato}}.</li><li>Es {{c2::universal}} y {{c2::limitante}}.</li></ul><div style="text-align: left;">
    (\downarrow\)&nbsp;</div><br><b>{{c1::Lengua}}:</b><br><ul style="">
    <li style="">{{c3::Sistema de signos linguisticos}} que da forma particular {{c3::al lenguaje}} en {{c3::una comunidad nacional}} o {{c3::supranacional}}.</li>
    <li style="">Es {{c3::abstracta}} y {{c3::evoluciona históricamente}}.</li></ul>\(\downarrow\)&nbsp;<br><br><b>{{c1::Idioma}}:&nbsp;</b><br>
    <ul style=""><li style="">{{c4::Lengua natural}} caracterizada {{c4::politicamente}} ({{c4::extralingsticamente}}).&nbsp;</li>
    <li style="">{{c4::Sistema linguístico}} definido en {{c4::términos extralingsticos}}.</li>
    <li style="">Es {{c4::la lengua oficial}} de {{c4::una nacion}}.</li></ul>\(\downarrow\)&nbsp;<b><br><br>{{c1::Dialecto}}:</b><br>
    <ul style=""><li style="">Variante {{c5::geografico-social}} de una {{c5::lengua}} dentro de {{c5::suírea dialectal}}.</li></ul>
    (\downarrow\)&nbsp;<b><br><br>{{c1::Habla}}:</b><br><ul style=""><li style="">{{c5::Uso}} del {{c5::sistema linguistico}}.</li>
    """

    res = tested._createFieldsContext(content, 1)

    assert ('c1::' not in res.effectiveText)
    assert ('c4::' not in res.effectiveText)
    assert ('c5::' not in res.effectiveText)


def test_issue_14():
    reviewer.card.note()['Text'] = """
<center><table class="highlighttable"><tbody><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">1
2</pre></div></td><td class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span style="color: #008000; font-weight: bold">def</span> test():
{{c1::Print(<span style="font-family: &quot;DejaVu Sans&quot;; color: rgb(186, 33, 33);">"Test"</span><span style="font-family: &quot;DejaVu Sans&quot;;">)}}</span>
</pre></div>
</td></tr></tbody></table></center><br>
    """

    res = reviewer.typeAnsQuestionFilter("""
        <span class="content">
        [[type:cloze:Text]]
        </span>
    """)

    print(res)


def test_issue_82():
    txt = """
<table class="table_class_basic_full_width"
       style="font-size: 85%; width: 100%; border-collapse: collapse; border: 1px solid;">
    <thead>
    <tr>
        <th style="width:8%; text-align:left; padding: 2px; border: 1px solid;">Geschäftsfall</th>
        <th style="width:8%; text-align:left; padding: 2px; border: 1px solid;">USt</th>
        <th style="width:8%; text-align:left; padding: 2px; border: 1px solid;">Ust Wert</th>
        <th style="width:8%; text-align:left; padding: 2px; border: 1px solid;">Netto</th>
        <th style="width:8%; text-align:left; padding: 2px; border: 1px solid;">Brutto</th>
        <th style="width:8%; text-align:left; padding: 2px; border: 1px solid;">Konten</th>
        <th style="width:8%; text-align:left; padding: 2px; border: 1px solid;">A/P</th>
        <th style="width:8%; text-align:left; padding: 2px; border: 1px solid;">EA/EE</th>
        <th style="width:8%; text-align:left; padding: 2px; border: 1px solid;">+/ -</th>
        <th style="width:8%; text-align:left; padding: 2px; border: 1px solid;">S/H</th>
        <th style="width:8%; text-align:left; padding: 2px; border: 1px solid;">Buchungssatz</th>
        <th style="width:8%; text-align:left; padding: 2px; border: 1px solid;">Soll</th>
        <th style="width:8%; text-align:left; padding: 2px; border: 1px solid;">Haben</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td style="width: 8%; padding: 2px; border: 1px solid;">Q/KB: Fachzeitschriften</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c1::x}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c1::x}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c1::x}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c1::x}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c1::Kasse}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c1::A}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c1::x}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c1::-}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c1::h}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c1::Fachz}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c1::35,05}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c1::x}}</td>
    </tr>
    <tr>
        <td style="width: 8%; padding: 2px; border: 1px solid;">bar bezahlt&nbsp;&nbsp;&nbsp; 37,5</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c2::7%}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c2::2,45}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c2::35,05}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c2::37,50}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">
            <table>
                <tbody>
                <tr>
                    <td>{{c2::Fachzeitschriften/Bücher}}</td>
                </tr>
                </tbody>
            </table>
        </td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c2::x}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c2::EA}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c2::+}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c2::s}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c2::Vst}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c2::2,45}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c2::x}}</td>
    </tr>
    <tr>
        <td style="width: 8%; padding: 2px; border: 1px solid;"></td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c2::x}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c2::x}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c2::x}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c2::x}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c2::Vst}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c2::A}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c2::x}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c2::+}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c2::s}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c2::an Kasse}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c2::x}}</td>
        <td style="width: 8%; padding: 2px; border: 1px solid;">{{c2::37,50}}</td>
    </tr>
    </tbody>
</table>
    """

    res = tested._createFieldsContext(txt, 1)
    assert ('c2::' not in res.effectiveText)
