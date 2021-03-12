from typing import List, Optional, Tuple, Callable

from natto import MeCab
from natto.node import MeCabNode as MeCabToken
import dataclasses

NODE_FORMAT_PREFIX = '%ps\\t%pe\\t'
DEFAULT_NODE_FORMAT = '%H\\n'


@dataclasses.dataclass()
class Token:

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
    additional_entries: List[str] = dataclasses.field(default_factory=list)
    start: Optional[int] = None
    end: Optional[int] = None

    def __str__(self) -> str:
        return self.surface

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)


def pre_parse(mecab_token: MeCabToken) -> Tuple[str, Optional[int], Optional[int], Optional[str]]:
    if mecab_token.is_eos():
        return '', None, None, 'BOS/EOS'
    s, e, fs = mecab_token.feature.split('\t')
    return mecab_token.surface, int(s), int(e), fs


def token_converter(mecab_token: MeCabToken, code_point: List[int], start_position: int) -> Token:
    surface, s, e, features = pre_parse(mecab_token)
    fs = features.split(',')

    (pos1, pos2, pos3, pos4, conjugation_form, conjugation_type, base_form, reading, pronunciation) = \
        list(map(lambda f: None if f == '*' else f, fs[0:9])) + [None, ] * max(0, 9 - len(fs))

    if surface == '' and pos1 == 'BOS/EOS':
        return PyMecab.EOS

    s = s - start_position
    e = e - start_position

    return Token(surface, pos1, pos2, pos3, pos4, conjugation_form, conjugation_type, base_form, reading,
                 pronunciation, additional_entries=fs[9:], start=code_point[s], end=code_point[e])


def parse_code_point(text: str) -> List[int]:
    code_point = [0 for _ in text.encode('utf-8')]
    s = 0
    for i, ch in enumerate(text):
        length = len(ch.encode('utf-8'))
        for b in range(s, s + length):
            code_point[b] = i
        s += length
    if code_point:
        code_point.append(code_point[-1] + 1)
    return code_point


class PyMecab:

    BOS: Token = Token('', 'BOS')
    EOS: Token = Token('', 'EOS')

    def __init__(self, options: str = None, node_format: str = DEFAULT_NODE_FORMAT, converter: Callable = None, **kwargs):
        options = options or ''
        self.__impl = MeCab(options=options + ' --node-format=' + NODE_FORMAT_PREFIX + node_format, **kwargs)
        self.__converter = converter or token_converter

    def tokenize(self, text: str) -> List[Token]:
        return self.__call__(text)

    def __call__(self, text: str) -> List[Token]:
        code_point = parse_code_point(text)

        results = []
        start_position = None
        for t in self.__impl.parse(text, as_nodes=True):
            if start_position is None:
                _, start_position, _, _ = pre_parse(t)
            token = self.__converter(t, code_point, start_position)
            results.append(token)

        return results
