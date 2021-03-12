# PyMecab
 
 [Mecab](http://taku910.github.io/mecab/) python wrapper by using [natto-py](https://github.com/buruzaemon/natto-py)


## Installations

### Pre Requirements

You need install mecab before installing PyMecab.
If your operating system is Mac OS and use homebrew, you can easily install both mecab and ipadic dictionary as follows:

```
brew install mecab
brew install mecab-ipadic
```

You can build a docker image by our [Dockerfile](https://github.com/jxpress/pymecab/blob/master/Dockerfile).

### Installation PyMecab 

```
pip install pymecab
```


## Usage


PyMecab provides you to easily access all part-of-speech features of mecab tokens on your code.

The sample code is as follows:

```python
from pymecab.pymecab import PyMecab


text = 'テクノロジーで「ビジネスとジャーナリズムの両立」を実現する'

mecab = PyMecab()

for token in mecab.tokenize(text):
    print(token.surface, token.pos1)
    
```

or

You can use simple console script `pymecab.console`

```

>  echo 'テクノロジーで「ビジネスとジャーナリズムの両立」を実現する' | pymecab.console                                                                                                                                                                                                                                                                                                                                 ⎈ (minikube/leo)

```

The output of above sample codes are:

```
テクノロジー 名詞
で 助詞
「 記号
ビジネス 名詞
と 助詞
ジャーナリズム 名詞
の 助詞
両立 名詞
」 記号
を 助詞
実現 名詞
する 動詞
 EOS
```
