import sys

from pymecab.pymecab import PyMecab, Token



def main():
    mecab = PyMecab()
    for text in sys.stdin.readlines():
        for token in mecab(text):
            print(token.surface, token.pos1)


if __name__ == "__main__":
    main()
