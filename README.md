# PyMecab
 
 [Mecab](http://taku910.github.io/mecab/) python wrapper by using [natto-py](https://github.com/buruzaemon/natto-py)


## Installation
 
```
pip install pymecab
```

## Usage

```python
# -*- coding: UTF-8 -*-

from pymecab.pymecab import PyMecab


text = 'テクノロジーで「ビジネスとジャーナリズムの両立」を実現する'

mecab = PyMecab()

for token in mecab.tokenize(text):
    print(token.surface, token.pos1)
    
```

