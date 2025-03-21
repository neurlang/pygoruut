# pygoruut

## Getting started

```python
from pygoruut.pygoruut import Pygoruut

pygoruut = Pygoruut()

print(str(pygoruut.phonemize(language="English", sentence="fast racing car")))

# Prints: fˈæst ˈɹeɪsɪŋ kɑː

# Now, convert it back

print(str(pygoruut.phonemize(language="English", sentence="fˈæst ˈɹeɪsɪŋ kɑː", is_reverse=True)))

# Prints: fast racing carr

```

### Uyghur language, our highest quality language

```python
print(str(pygoruut.phonemize(language="Uyghur", sentence="قىزىل گۈل ئاتا")))

# Prints: qɯzɤl gyl ʔɑtɑ

# Now, convert it back

print(str(pygoruut.phonemize(language="Uyghur", sentence="qizil gyl ʔɑtɑ", is_reverse=True)))

# Prints: قىزىل گۈل ئاتا

```

The quality of translation varies accros the 136 supported languages.

## Advanced Use

### Multi lingual sentences handling

Use comma (,) separated languages in language (the first language is the preferred language):

```python
print(pygoruut.phonemize(language="English,Slovak", sentence="hello world ahojte not-in-dictionary!!!!"))

# Prints: hɛlˈoʊ wəld aɦɔjcɛ --nˈoʊtˈinnikʃənɑɹɪ!!!!
```

### No punctuation

```python
' '.join([w.Phonetic for w in pygoruut.phonemize(language="English", sentence="hello world!!!!").Words])
```

### Force a specific version

A certain version is frozen, it will translate all words in the same way

```python
from pygoruut.pygoruut import Pygoruut

pygoruut = Pygoruut(version='v0.5.1')

```

### Configure a model download directory for faster startup

For faster startup, the model can be cached in the user-provided directory

```python
from pygoruut.pygoruut import Pygoruut

pygoruut = Pygoruut(writeable_bin_dir='/home/john/')
```

If you want to cache it in user's home subdir .goruut, use:

```python
from pygoruut.pygoruut import Pygoruut

pygoruut = Pygoruut(writeable_bin_dir='')
```
