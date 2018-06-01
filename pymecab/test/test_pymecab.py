# -*- coding: UTF-8 -*-

from pymecab.pymecab import PyMecab


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
        fs(token.pronunciation)
    ]
    return '%s\t%s' % (token.surface, ','.join(features)) 


def test_mecab():
    text = '太郎は昨日、本を買った'

    expect = [
    '太郎\t名詞,固有名詞,人名,名,*,*,太郎,タロウ,タロー',
    'は\t助詞,係助詞,*,*,*,*,は,ハ,ワ',
    '昨日\t名詞,副詞可能,*,*,*,*,昨日,キノウ,キノー',
    '、\t記号,読点,*,*,*,*,、,、,、',
    '本\t名詞,一般,*,*,*,*,本,ホン,ホン',
    'を\t助詞,格助詞,一般,*,*,*,を,ヲ,ヲ',
    '買っ\t動詞,自立,*,*,五段・ワ行促音便,連用タ接続,買う,カッ,カッ',
    'た\t助動詞,*,*,*,特殊・タ,基本形,た,タ,タ',
    '\tEOS,*,*,*,*,*,*,*,*'
    ]

    tokenizer = PyMecab()
    actual = [token_to_str(token) for token in tokenizer(text)]
    assert len(actual) == len(expect)

    for i in range(len(expect)):
        assert actual[i] == expect[i]


def test_change_options():
    text = '太郎は昨日、本を買った'
    tokenizer = PyMecab('-N 2')
    results = [token  for token in tokenizer(text) if token.pos1 == 'EOS']
    assert len(results) == 2


def test_additional_entries():
    from collections import namedtuple
    DummyMecabToken = namedtuple('DummyMecabToken', ('surface', 'feature'))
    mecab_token = DummyMecabToken(surface='三代目', feature='名詞,固有名詞,一般,*,*,*,3代目,サンダイメ,サンダイメ,[:_:919    910    8281]')

    expect = '三代目\t名詞,固有名詞,一般,*,*,*,3代目,サンダイメ,サンダイメ'
    tokenizer = PyMecab()
    token = tokenizer._PyMecab__convert(mecab_token)
    assert expect == token_to_str(token)
    assert token.additional_entries == ['[:_:919    910    8281]']





