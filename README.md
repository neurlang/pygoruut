# pygoruut

## Getting started

```
from pygoruut.pygoruut import Pygoruut

pygoruut = Pygoruut()

print(pygoruut.phonemize(language="English", sentence="fast racing car"))

# Prints:
# PhonemeResponse(Words=[
#  Word(CleanWord='fast', Phonetic='fˈæst'),
#  Word(CleanWord='racing', Phonetic='ˈɹeɪsɪŋ'),
#  Word(CleanWord='car', Phonetic='kɑː')])

# Now, convert it back

print(pygoruut.phonemize(language="English", sentence="fˈæst ˈɹeɪsɪŋ kɑː", is_reverse=True))

# Prints:
# PhonemeResponse(Words=[
#  Word(CleanWord='fˈæst', Phonetic='fast'),
#  Word(CleanWord='ˈɹeɪsɪŋ', Phonetic='racing'),
#  Word(CleanWord='kɑː', Phonetic='carr')])

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

## Advanced Use

### Force a specific version

A certain version is frozen, it will translate all words in the same way

```
from pygoruut.pygoruut import Pygoruut

pygoruut = Pygoruut(version='0.4.0')

```

### Configure a model download directory for faster startup

For faster startup, the model can be cached in the user-provided directory

```
from pygoruut.pygoruut import Pygoruut

pygoruut = Pygoruut(writeable_bin_dir='/home/john/')
```


