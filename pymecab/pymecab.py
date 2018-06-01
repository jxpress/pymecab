from typing import NamedTuple, List

from natto import MeCab


class Token(NamedTuple):

    surface: str = None

    pos1: str = None
    pos2: str = None
    pos3: str = None
    pos4: str = None

    conjugation_form: str = None
    conjugation_type: str = None
    base_form: str = None
    reading: str = None
    pronunciation: str = None
    additional_entries: List[str] = []

    def __str__(self) -> str:
        return self.surface


class PyMecab:

    BOS = Token('', 'BOS')
    EOS = Token('', 'EOS')

    def __init__(self, options=None, **kwargs):
        self.__impl = MeCab(options=options, **kwargs)

    def __convert(self, mecab_token):
        surface = mecab_token.surface
        features = mecab_token.feature.split(',')
        fs = features[0:9]

        (pos1, pos2, pos3, pos4, conjugation_form, conjugation_type, base_form, reading, pronunciation) = \
            list(map(lambda f: None if f == '*' else f, fs)) + [None,] * max(0, 9 - len(fs))

        if surface == '' and pos1 == 'BOS/EOS':
            return PyMecab.EOS

        return Token(surface, pos1, pos2, pos3, pos4, conjugation_form, conjugation_type, base_form, reading,
                            pronunciation, additional_entries=features[9:])

    def tokenize(self, text: str) -> List[Token]:
        return self.__call__(text)

    def __call__(self, text: str) -> List[Token]:
        return [self.__convert(t) for t in self.__impl.parse(text, as_nodes=True)]
