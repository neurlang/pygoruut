import subprocess
import os
import time
import requests
from dataclasses import dataclass, field
from typing import List
from pygoruut.executable import MyPlatformExecutable
from pygoruut.pygoruut_languages import PygoruutLanguages
from pygoruut.config import Config, ConfigApi
import tempfile
from pathlib import Path

class PathContext(str):
    """A string-like path that supports the context manager protocol."""
    def __init__(self, path):
        self.path = path
        self.original_dir = os.getcwd()

    def __enter__(self):
        # Change directory (or perform other setup)
        os.chdir(self.path)
        return self  # Return self to allow using the object directly

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore original directory (or cleanup)
        os.chdir(self.original_dir)

    # Optional: Implement __fspath__ for os.PathLike compatibility
    def __fspath__(self):
        return str(self.path)

@dataclass
class Word:
    CleanWord: str
    Phonetic: str
    PosTags: List[str]
    PrePunct: str
    PostPunct: str
    IsFirst: bool
    IsLast: bool
    def __init__(self, CleanWord: str, Phonetic: str, Linguistic: str = None, PostPunct: str = "", PrePunct: str = "", PosTags: List[str] = [], IsFirst = None, IsLast = None):
        self.CleanWord = CleanWord
        self.Phonetic = Phonetic
        self.PosTags = PosTags
        self.PrePunct = PrePunct
        self.PostPunct = PostPunct
        self.IsFirst = IsFirst
        self.IsLast = IsLast

@dataclass
class PhonemeResponse:
    Words: List[Word]
    Separator: str
    def __str__(self):
        return self.Separator.join([w.PrePunct + w.Phonetic + w.PostPunct for w in self.Words])

class Pygoruut:
    def __init__(self, version=None, writeable_bin_dir=None, api=None, models={}):
        if api is None:
            self.executable, self.platform, self.version = MyPlatformExecutable(version).get()
        else:
            self.executable = None
        if self.executable is None:
            if api is not None:
                self.executable = None
                self.platform = None
                self.version = None
                self.process = None
                self.config = ConfigApi(api)
                return
            elif version is None:
                raise ValueError(f"Unsupported goruut architecture")
            else:
                raise ValueError(f"Unsupported goruut architecture or version: {version}")
        if writeable_bin_dir == "":
            # Get the user's home directory
            home_dir = Path.home()
            # Define the name of the hidden directory
            hidden_dir_name = ".goruut"
            # Create the full path for the hidden directory
            hidden_dir_path = home_dir / hidden_dir_name
            # Create the hidden directory (if it doesn't already exist)
            hidden_dir_path.mkdir(exist_ok=True)
            writeable_bin_dir = str(hidden_dir_path)
        with PathContext(writeable_bin_dir) if writeable_bin_dir else tempfile.TemporaryDirectory() as temp_dir:
            try:
                self.executable_path = self.executable.exists(temp_dir)
            except Exception as e:
                self.executable_path = self.executable.download(temp_dir)
            self.config = Config()
            self.config.serialize(os.path.join(temp_dir, "goruut_config.json"), models)
            self.process = subprocess.Popen([self.executable_path, "--configfile", os.path.join(temp_dir, "goruut_config.json")],
                #stdout=subprocess.PIPE,  # Redirect stdout to capture it
                stderr=subprocess.PIPE,  # (Optional) Redirect stderr if you want to capture errors
                text=True  # Ensure the output is in text mode (instead of bytes)
            )
            # Read stdout line by line
            while True:
                output = self.process.stderr.readline()
                if output == '' and self.process.poll() is not None:
                    break  # If process has ended and no output is left, stop
                if 'Serving...' in output:
                    #print("Process running")
                    break  # Stop when the substring is found
                #if output:
                #    #print(output.strip())  # Print subprocess output for tracking purposes
            url = self.config.url("tts/phonemize/sentence")
            response = requests.post(url, json={}, timeout=(10, 30))
            response.raise_for_status()

    def exact_version(self) -> str:
        return self.version

    def compatible_version(self) -> str:
        return self.version.rstrip('0123456789')
    
    def __del__(self):
        if hasattr(self, 'process') and self.process is not None:
            self.process.terminate()
            self.process.wait()

    def phonemize(self, language="Greek", sentence="Σήμερα...", is_reverse=False, separator=" ", is_punct=True) -> PhonemeResponse:
        if ',' in language:
            languages = [PygoruutLanguages()[l] for l in language.split(',')]
            language = ""
        else:
            languages = []
            # handle ISO here
            language = PygoruutLanguages()[language]
        url = self.config.url("tts/phonemize/sentence")
        payload = {"Language": language, "Languages": languages, "Sentence": sentence, "IsReverse": is_reverse}

        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        data = response.json()

        if is_punct:
            words = [Word(**word) for word in data["Words"]]
        else:
            words = [Word(**{**word, "PrePunct": "", "PostPunct": ""}) for word in data["Words"]]
        return PhonemeResponse(Words=words, Separator=separator)
