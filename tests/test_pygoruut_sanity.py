import unittest
import time
from pygoruut.pygoruut import Pygoruut

class TestPygoruutSanity(unittest.TestCase):
    def setUp(self):
        self.pygoruut = Pygoruut()

    def tearDown(self):
        del self.pygoruut

    def test_languages_and_word_pairs(self):
        test_cases = [
            ("el", [
                ("Σήμερα", "simera"),
                ("καλημέρα", "kalimera"),
                ("ευχαριστώ", "efxaristo")
            ]),
            ("English", [
                ("hello", "hˈɛlloʊ"),
                ("world", "wˈɚld"),
                ("python", "piθən")
            ]),
            ("Spanish", [
                ("hola", "ˌeolˌa"),
                ("mundo", "mˈuˈnðo"),
                ("gracias", "gɾakiasˈ")
            ]),
            ("fr", [
                ("bonjour", "bɔ̃ʒˈuʁ"),
                ("monde", "mɔ̃dʁ"),
                ("merci", "mʁkˈɪ")
            ]),
            ("German", [
                ("hallo", "hˈallˈɔ"),
                ("welt", "vəlt"),
                ("danke", "dˈankə")
            ])
        ]

        for language, word_pairs in test_cases:
            with self.subTest(language=language):
                for input_word, expected_phonetic in word_pairs:
                    with self.subTest(input_word=input_word):
                        try:
                            response = self.pygoruut.phonemize(language, input_word)
                            self.assertIsNotNone(response)
                            self.assertTrue(len(response.Words) > 0)
                            actual_word = response.Words[0]
                            
                            self.assertEqual(actual_word.CleanWord.lower(), input_word.lower())
                            self.assertEqual(actual_word.Phonetic, expected_phonetic)
                            
                            print(f"Successful phonemization for {language} word '{input_word}':")
                            print(f"  Expected: {expected_phonetic}")
                            print(f"  Actual:   {actual_word.Phonetic}")
                        except AssertionError as e:
                            print(f"Assertion failed for {language} word '{input_word}':")
                            print(f"  Expected: {expected_phonetic}")
                            print(f"  Actual:   {actual_word.Phonetic}")
                            raise e
                        except Exception as e:
                            self.fail(f"Phonemization failed for {language} word '{input_word}': {str(e)}")

if __name__ == '__main__':
    unittest.main()
