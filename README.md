# Jaundiced news filter

Only one news site is supported so far - [INOSMI.RU](https://inosmi.ru/). For that one, a special adapter has been developed to highlight the text of an article against the rest of the HTML markup. Other news sites will require new adapters, all of which are located in the `adapters` directory. The code for the INOSMI.ru site is placed there, too: `adapters/inosmi_ru.py`.

In the future, you can create a universal adapter suitable for all sites, but its development will be complicated and require additional time and effort.

# How to run server

You will need Python 3.9 or later. It is recommended to create a virtual environment to install packages.

The first step is to install the packages:


```
pip3 install -r requirements.txt
```

# How to run

```
python3 server.py
```

# How to run tests

For testing use [pytest](https://docs.pytest.org/en/latest/) The command to run the tests:


```
python -m pytest
```

# Project goals

The code is written for training purposes. This is a lesson from a web development course - [Devman](https://dvmn.org).

