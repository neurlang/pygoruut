# pygoruut

## Getting started

```
from pygoruut.pygoruut import Pygoruut

pygoruut = Pygoruut()

print(pygoruut.phonemize(language="English", sentence="hello world"))

# Prints:
# PhonemeResponse(
#     Words=[Word(CleanWord='hello', Linguistic='hello', Phonetic='hɛloʊ'),
#            Word(CleanWord='world', Linguistic='world', Phonetic='wɚld')])
```
