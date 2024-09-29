import unittest
import time
from pygoruut import Pygoruut

class TestPygoruutSanity(unittest.TestCase):
    def setUp(self):
        self.pygoruut = Pygoruut()

    def tearDown(self):
        del self.pygoruut

    def test_languages_and_word_pairs(self):
        test_cases = [
            ("Greek", [
                ("Σήμερα", "sime̞ɾɐ"),
                ("καλημέρα", "kalime̞ɾa"),
                ("ευχαριστώ", "e̞fxaɾisto")
            ]),
            ("English", [
                ("hello", "hɛloʊ"),
                ("world", "wɚld"),
                ("python", "piθən")
            ]),
            ("Spanish", [
                ("hola", "ola"),
                ("mundo", "mundo"),
                ("gracias", "gɾakias")
            ]),
            ("French", [
                ("bonjour", "bonʒuʁ"),
                ("monde", "mod"),
                ("merci", "mɛʁki")
            ]),
            ("German", [
                ("hallo", "halloː"),
                ("welt", "vəlt"),
                ("danke", "dankə")
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
