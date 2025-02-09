# pygoruut

## Getting started

```
from pygoruut.pygoruut import Pygoruut

pygoruut = Pygoruut()

print(pygoruut.phonemize(language="English", sentence="fast racing car"))

# Prints:
# PhonemeResponse(Words=[
#  Word(CleanWord='fast', Phonetic='fəst'),
#  Word(CleanWord='racing', Phonetic='ɹəkɪŋ'),
#  Word(CleanWord='car', Phonetic='kəɹ')])

# Now, convert it back

print(pygoruut.phonemize(language="English", sentence="fəst ɹəkɪŋ kəɹ", is_reverse=True))

# Prints:
# PhonemeResponse(Words=[
#  Word(CleanWord='fəst', Phonetic='fast'),
#  Word(CleanWord='ɹəkɪŋ', Phonetic='racing'),
#  Word(CleanWord='kəɹ', Phonetic='car')])

```

### Uyghur language, our highest quality language

```
print(pygoruut.phonemize(language="Uyghur", sentence="قىزىل گۈل ئاتا"))

# Prints:
# PhonemeResponse(Words=[
#  Word(CleanWord='قىزىل', Phonetic='qizil'),
#  Word(CleanWord='گۈل', Phonetic='gyl'),
#  Word(CleanWord='ئاتا', Phonetic='ʔɑtɑ')])

# Now, convert it back

print(pygoruut.phonemize(language="Uyghur", sentence="qizil gyl ʔɑtɑ", is_reverse=True))

# Prints:
# PhonemeResponse(Words=[
#  Word(CleanWord='qizil', Phonetic='قىزىل'),
#  Word(CleanWord='gyl', Phonetic='گۈل'),
#  Word(CleanWord='ʔɑtɑ', Phonetic='ئاتا')])

```

The quality of translation varies accros the 85 supported languages.
