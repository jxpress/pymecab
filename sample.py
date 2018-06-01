# -*- coding: UTF-8 -*-

from pymecab.pymecab import PyMecab

if __name__ == "__main__":
    text = 'テクノロジーで「ビジネスとジャーナリズムの両立」を実現する'

    mecab = PyMecab()

    for token in mecab(text):
        print(token, token.pos1)
