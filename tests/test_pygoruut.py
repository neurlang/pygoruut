import unittest
from unittest.mock import patch, MagicMock
from pygoruut.pygoruut import Pygoruut, PhonemeResponse, Word


class TestPygoruut(unittest.TestCase):
    @patch('pygoruut.pygoruut.MyPlatformExecutable')  # Patch MyPlatformExecutable
    @patch('pygoruut.pygoruut.Config')  # Patch Config class
    @patch('subprocess.Popen')  # Patch subprocess.Popen
    def test_init(self, mock_popen, mock_config, mock_executable):
        # Mock MyPlatformExecutable's get method
        mock_executable.return_value.get.return_value = (MagicMock(), 'test_platform', 'test_version')

        # Mock Popen to simulate a process that will print 'Serving...'
        mock_process = MagicMock()
        mock_process.stderr.readline.side_effect = ['Serving...\n', '']
        mock_process.poll.return_value = None
        mock_popen.return_value = mock_process

        pygoruut = Pygoruut(writeable_bin_dir='')

        # Assert Popen was called with expected arguments
        mock_popen.assert_called_once()

        # Check if 'Serving...' was found
        mock_process.stderr.readline.assert_called()

    @patch('pygoruut.pygoruut.MyPlatformExecutable')  # Patch MyPlatformExecutable
    @patch('pygoruut.pygoruut.Config')  # Patch Config class
    @patch('subprocess.Popen')  # Patch subprocess.Popen
    def test_del(self, mock_popen, mock_config, mock_executable):
        # Mock MyPlatformExecutable's get method
        mock_executable.return_value.get.return_value = (MagicMock(), 'test_platform', 'test_version')

        # Mock Popen to simulate a subprocess
        mock_process = MagicMock()
        mock_process.stderr.readline.side_effect = ['Serving...\n', '']
        mock_process.poll.return_value = None
        mock_popen.return_value = mock_process

        pygoruut = Pygoruut(writeable_bin_dir='')

        # Test the destructor (when the object is deleted)
        del pygoruut

        # Ensure terminate and wait were called
        mock_process.terminate.assert_called_once()
        mock_process.wait.assert_called_once()

    @patch('requests.post')
    def test_phonemize(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Words": [
                {
                    "CleanWord": "σήμερα",
                    "Phonetic": "ˈsimira"
                }
            ]
        }
        mock_post.return_value = mock_response

        pygoruut = Pygoruut(writeable_bin_dir='')
        result = pygoruut.phonemize()

        self.assertIsInstance(result, PhonemeResponse)
        self.assertEqual(len(result.Words), 1)
        self.assertEqual(result.Words[0].CleanWord, "σήμερα")
        self.assertEqual(result.Words[0].Phonetic, "ˈsimira")

        mock_post.assert_called_once_with(
            pygoruut.config.url("tts/phonemize/sentence"),
            json={"Language": "Greek", "Languages": [], "Sentence": "Σήμερα...", "IsReverse": False}
        )

if __name__ == '__main__':
    unittest.main()
