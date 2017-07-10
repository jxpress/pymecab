from collections import namedtuple
from natto import MeCab


Token = namedtuple('Token', ('surface', 'pos1', 'pos2', 'pos3', 'pos4', 'conjugation_form', 'conjugation_type', 'base_form', 'reading', 'pronunciation'))

Token.__new__.__defaults__ = (None, None, None, None, None, None, None, None, None, None)


class PyMecab:

    BOS = Token('', 'BOS', None, None, None, None, None, None, None, None)
    EOS = Token('', 'EOS', None, None, None, None, None, None, None, None)

    def __init__(self, options=None, **kwargs):
        self.mecab = MeCab(options=None, kwargs=kwargs)

    def __convert(self, mecab_token):
        surface = mecab_token.surface
        fs = mecab_token.feature.split(',')

        (pos1, pos2, pos3, pos4, conjugation_form, conjugation_type, base_form, reading, pronunciation) = \
            list(map(lambda f: None if f == '*' else f, fs)) + [None,] * max(0, 9 - len(fs))

        if surface == '' and pos1 == 'BOS/EOS':
            return PyMecab.EOS

        return Token(surface, pos1, pos2, pos3, pos4, conjugation_form, conjugation_type, base_form, reading,
                            pronunciation)

    def tokenize(self, text):
        return [self.__convert(t) for t in self.mecab.parse(text, as_nodes=True)]
