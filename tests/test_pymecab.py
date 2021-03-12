from typing import List

import pytest
from pymecab.pymecab import PyMecab, parse_code_point




def fs(x):
    return x if x is not None else '*' 


def token_to_str(token):
    features = [
        fs(token.pos1),
        fs(token.pos2),
        fs(token.pos3),
        fs(token.pos4),
        fs(token.conjugation_form),
        fs(token.conjugation_type),
        fs(token.base_form),
        fs(token.reading),
        fs(token.pronunciation),
    ]
    s = token.start
    e = token.end
    if s is None:
        s = ''
    if e is None:
        e = ''
    return f"{token.surface}\t{s}\t{e}\t{','.join(features)}"


def check_results(text: str, expect: List[str], tokenizer = None):
    tokenizer = tokenizer or PyMecab()
    actual = [token_to_str(token) for token in tokenizer(text)]
    assert len(actual) == len(expect)

    for i in range(len(expect)):
        assert actual[i] == expect[i]


def test_mecab():
    text = '太郎は昨日、本 を買った'

    expect = [
        '太郎\t0\t2\t名詞,固有名詞,人名,名,*,*,太郎,タロウ,タロー',
        'は\t2\t3\t助詞,係助詞,*,*,*,*,は,ハ,ワ',
        '昨日\t3\t5\t名詞,副詞可能,*,*,*,*,昨日,キノウ,キノー',
        '、\t5\t6\t記号,読点,*,*,*,*,、,、,、',
        '本\t6\t7\t名詞,一般,*,*,*,*,本,ホン,ホン',
        'を\t8\t9\t助詞,格助詞,一般,*,*,*,を,ヲ,ヲ',
        '買っ\t9\t11\t動詞,自立,*,*,五段・ワ行促音便,連用タ接続,買う,カッ,カッ',
        'た\t11\t12\t助動詞,*,*,*,特殊・タ,基本形,た,タ,タ',
        '\t\t\tEOS,*,*,*,*,*,*,*,*'
    ]
    check_results(text, expect)


def test_change_options():
    text = '太郎は昨日、本を買った'
    tokenizer = PyMecab('-N 2')
    results = [token for token in tokenizer(text) if token.pos1 == 'EOS']
    assert len(results) == 2


def test_additional_entries():
    import dataclasses
    from collections import namedtuple

    @dataclasses.dataclass()
    class DummyMecabToken:
        surface: str
        feature: str

        def is_eos(self) -> bool:
            return False

    mecab_token = DummyMecabToken(surface='三代目', feature="10\t17\t名詞,固有名詞,一般,*,*,*,3代目,サンダイメ,サンダイメ,[:_:919    910    8281]")
    code_point = parse_code_point('三代目')

    expect = '三代目\t0\t2\t名詞,固有名詞,一般,*,*,*,3代目,サンダイメ,サンダイメ'
    tokenizer = PyMecab()
    token = tokenizer._PyMecab__converter(mecab_token, code_point, 10)
    assert expect == token_to_str(token)
    assert token.additional_entries == ['[:_:919    910    8281]']


def test_multi_sentences():
    text1 = '太郎は昨日、本 を買った'
    text2 = '花子 も同じ本 を読んだ'

    expect1 = [
        '太郎\t0\t2\t名詞,固有名詞,人名,名,*,*,太郎,タロウ,タロー',
        'は\t2\t3\t助詞,係助詞,*,*,*,*,は,ハ,ワ',
        '昨日\t3\t5\t名詞,副詞可能,*,*,*,*,昨日,キノウ,キノー',
        '、\t5\t6\t記号,読点,*,*,*,*,、,、,、',
        '本\t6\t7\t名詞,一般,*,*,*,*,本,ホン,ホン',
        'を\t8\t9\t助詞,格助詞,一般,*,*,*,を,ヲ,ヲ',
        '買っ\t9\t11\t動詞,自立,*,*,五段・ワ行促音便,連用タ接続,買う,カッ,カッ',
        'た\t11\t12\t助動詞,*,*,*,特殊・タ,基本形,た,タ,タ',
        '\t\t\tEOS,*,*,*,*,*,*,*,*'
    ]
    expect2 = [
        '花子\t0\t2\t名詞,固有名詞,人名,名,*,*,花子,ハナコ,ハナコ',
        'も\t3\t4\t助詞,係助詞,*,*,*,*,も,モ,モ',
        '同じ\t4\t6\t連体詞,*,*,*,*,*,同じ,オナジ,オナジ',
        '本\t6\t7\t名詞,一般,*,*,*,*,本,ホン,ホン',
        'を\t8\t9\t助詞,格助詞,一般,*,*,*,を,ヲ,ヲ',
        '読ん\t9\t11\t動詞,自立,*,*,五段・マ行,連用タ接続,読む,ヨン,ヨン',
        'だ\t11\t12\t助動詞,*,*,*,特殊・タ,基本形,だ,ダ,ダ',
        '\t\t\tEOS,*,*,*,*,*,*,*,*'
    ]
    tokenizer = PyMecab()
    check_results(text1, expect1, tokenizer)
    check_results(text2, expect2, tokenizer)
