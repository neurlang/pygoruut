# pygoruut

## Getting started

```
from pygoruut.pygoruut import Pygoruut

pygoruut = Pygoruut()

print(pygoruut.phonemize(language="English", sentence="hello world"))

# Prints:
# PhonemeResponse(Words=[
#  Word(CleanWord='hello', Phonetic='hˈɛlloʊ'),
#  Word(CleanWord='world', Phonetic='wˈɚld')])

```
