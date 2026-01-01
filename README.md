# pygoruut

## Getting started

```python
from pygoruut.pygoruut import Pygoruut

pygoruut = Pygoruut()

print(str(pygoruut.phonemize(language="EnglishAmerican", sentence="fast racing car")))

# Prints: fˈæst ɹˈeɪsɪŋ kˈɑɹ

# Now, convert it back

print(str(pygoruut.phonemize(language="EnglishAmerican", sentence="fˈæst ɹˈeɪsɪŋ kˈɑɹ", is_reverse=True)))

# Prints: fast racing car
```

> ℹ️ For English, we recommend using `EnglishBritish` or `EnglishAmerican` instead of `English`. These dialect-specific models use high-quality Kokoro Misaki dictionaries and produce better results, especially for reversing IPA back to text.

---

### Uyghur language, our highest quality language

```python
print(str(pygoruut.phonemize(language="Uyghur", sentence="قىزىل گۈل ئاتا")))

# Prints: qizil gyl ʔɑtɑ

# Now, convert it back

print(str(pygoruut.phonemize(language="Uyghur", sentence="qizil gyl ʔɑtɑ", is_reverse=True)))

# Prints: قىزىل گۈل ئاتا
```

The quality of translation varies across the 136 supported languages.

---

## Advanced Use

### Multi-lingual sentence handling

Use comma (`,`) separated languages in `language`. The first language is the preferred language:

```python
print(pygoruut.phonemize(language="EnglishBritish,Slovak", sentence="hello world ahojte notindictionary!!!!"))

# Prints: həlˈoʊ wˈɜɹld aɦɔjcɛ ŋətandəktɪnˈɑːɪ!!!!
```

---

### Numerics handling (English, Arabic)

```python
print(str(pygoruut.phonemize(language="EnglishBritish", sentence="100 bottles")))

# Prints: wˈʌn hˈʌndɹəd bˈɒtəlz
```

---

### Homograph handling (Hebrew3)

```python
print(str(pygoruut.phonemize(language="Hebrew3", sentence="השרים ביקשו מהשרים לפתוח את הדלתות של בית השרים.")))

# Prints: hasaʁˈim bikʃˈu mehasaʁˈim liftˈoaχ ʔˈet hadlatˈot ʃˈel bajˈit hasaʁˈim.
```

---

### No punctuation

```python
print(str(pygoruut.phonemize(language="EnglishBritish", sentence="hello world!!!!", is_punct=False)))

# Prints: həlˈoʊ əɹld
```

---

### Force a specific version

You can pin a specific version. It will translate all words in the same way forever:

```python
from pygoruut.pygoruut import Pygoruut

pygoruut = Pygoruut(version='v0.6.2')
```

---

### Use an online inference api

You can use an inference api. The model will not be downloaded:

```python
from pygoruut.pygoruut import Pygoruut

pygoruut = Pygoruut(api='https://hashtron.cloud')
```

---

### Use an extra model

Extra model can be loaded from a ZIP file manually. It extends a specific language.

```python
from pygoruut.pygoruut import Pygoruut

pygoruut = Pygoruut(models={"Hebrew3": "/home/john/Downloads/hebrew3.zip"})
```

---

### Configure a model download directory for faster startup

To cache models in a user-specified directory:

```python
from pygoruut.pygoruut import Pygoruut

pygoruut = Pygoruut(writeable_bin_dir='/home/john/')
```

To cache in the user's home subdirectory `.goruut`:

```python
from pygoruut.pygoruut import Pygoruut

pygoruut = Pygoruut(writeable_bin_dir='')
```
