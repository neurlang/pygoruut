import unittest
import time
from pygoruut.pygoruut import Pygoruut

class TestPygoruutSanity(unittest.TestCase):
    def setUp(self):
        self.pygoruut = Pygoruut(writeable_bin_dir='')

    def tearDown(self):
        del self.pygoruut

    def test_languages_and_word_pairs(self):
        test_cases = [
            # These have to be words which don't have multiple pronounces
            ("el", [
                ("σιμερα", "ziˈmɛra", False),
                ("καλιμερα", "kalimˈeˈˈa", False),
                ("ευχαριστώ", "efxaˈristɔ", False)
            ]),
            ("English", [
                ("hampered", "hˈæmpɚd", False),
                ("super", "sˈupɚ", False),
                ("python", "pˈaɪθɑn", False)
            ]),
            ("Spanish", [
                ("hola", "ˈola", False),
                ("mundo", "mˈundo", False),
                ("gracias", "gɾˈaθjas", False)
            ]),
            ("fr", [
                ("bonjour", "bɔ̃ʒˈuʁ", False),
                ("monde", "aɔ̃d", False),
                ("merci", "mɛʁsˈi", False)
            ]),
            ("German", [
                ("hallo", "hˈaloː", True),
                ("welt", "vˈɛlt", False),
                ("danke", "dˈaŋkə", False)
            ])
        ]

        for language, word_pairs in test_cases:
            with self.subTest(language=language):
                for input_word, expected_phonetic, _ in word_pairs:
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


        for language, word_pairs in test_cases:
            with self.subTest(language=language):
                for expected_word, input_phonetic, bidi in word_pairs:
                    if not bidi:
                        continue
                    with self.subTest(input_phonetic=input_phonetic):
                        try:
                            response = self.pygoruut.phonemize(language, input_phonetic, is_reverse=True)
                            self.assertIsNotNone(response)
                            self.assertTrue(len(response.Words) > 0)
                            actual_word = response.Words[0]
                            
                            self.assertEqual(actual_word.CleanWord.lower(), input_phonetic.lower())
                            self.assertEqual(actual_word.Phonetic, expected_word)
                            
                            print(f"Successful dephonemization for {language} IPA '{input_phonetic}':")
                            print(f"  Expected: {expected_word}")
                            print(f"  Actual:   {actual_word.Phonetic}")
                        except AssertionError as e:
                            print(f"Assertion failed for {language} IPA '{input_phonetic}':")
                            print(f"  Expected: {expected_word}")
                            print(f"  Actual:   {actual_word.Phonetic}")
                            raise e
                        except Exception as e:
                            self.fail(f"Dephonemization failed for {language} IPA '{input_phonetic}': {str(e)}")







if __name__ == '__main__':
    unittest.main()
