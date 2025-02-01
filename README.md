# pygoruut

## Getting started

```
from pygoruut.pygoruut import Pygoruut

pygoruut = Pygoruut()

print(pygoruut.phonemize(language="English", sentence="hello world"))

# Prints:
# PhonemeResponse(Words=[
#  Word(CleanWord='hello', Phonetic='hˈɛlloʊ'),
#  Word(CleanWord='world', Phonetic='wˈɔɹˈɛd')])

# Now, convert it back

print(pygoruut.phonemize(language="English", sentence="hɛlloʊ wɔɹɛd", is_reverse=True))

# Prints:
# PhonemeResponse(Words=[
#  Word(CleanWord='hɛlloʊ', Phonetic='hello'),
#  Word(CleanWord='wɔɹɛd', Phonetic='wored')])

```

The quality of translation varies accros the 85 supported languages.
