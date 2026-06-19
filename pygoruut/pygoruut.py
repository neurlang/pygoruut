import subprocess
import os
import time
import requests
import threading
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
                stderr=subprocess.PIPE,
                text=True
            )
            drainer = threading.Thread(target=self._drain_stderr, daemon=True)
            drainer.start()
            url = self.config.url("tts/phonemize/sentence")
            for _ in range(60):
                if self.process.poll() is not None:
                    raise RuntimeError("Phonemize server exited before becoming ready")
                try:
                    response = requests.post(url, json={}, timeout=0.5)
                    response.raise_for_status()
                    break
                except (requests.ConnectionError, requests.Timeout):
                    time.sleep(0.5)
            else:
                raise RuntimeError("Phonemize server did not start within 30 seconds")

    def _drain_stderr(self):
        try:
            for line in self.process.stderr:
                pass
        except Exception:
            pass

    def exact_version(self) -> str:
        return self.version

    def compatible_version(self) -> str:
        return self.version.rstrip('0123456789')
    
    def __del__(self):
        try:
            proc = self.process
        except AttributeError:
            return
        if proc is not None:
            try:
                proc.terminate()
                proc.wait()
            except Exception:
                pass

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
