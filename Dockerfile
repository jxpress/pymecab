FROM python:3.6

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y mecab libmecab-dev mecab-ipadic-utf8 \
    && apt-get clean \
    && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*


WORKDIR /root

ADD pymecab /root/pymecab
ADD setup.py /root

RUN ["/bin/bash", "-c", "pip install -e ."]

CMD ["/bin/bash", "-c", "pymecab.console"]
