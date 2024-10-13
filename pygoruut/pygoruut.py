import subprocess
import os
import time
import requests
from dataclasses import dataclass, field
from typing import List
from pygoruut.executable import MyPlatformExecutable
from pygoruut.pygoruut_languages import PygoruutLanguages
from pygoruut.config import Config
import tempfile

@dataclass
class Word:
    CleanWord: str
    Phonetic: str
    def __init__(self, CleanWord: str, Phonetic: str, Linguistic: str = None):
        self.CleanWord = CleanWord
        self.Phonetic = Phonetic

@dataclass
class PhonemeResponse:
    Words: List[Word]

class Pygoruut:
    def __init__(self, version=None):
        self.executable, self.platform, self.version = MyPlatformExecutable(version).get()
        if self.executable is None: 
            if version is None:
                raise ValueError(f"Unsupported goruut architecture")
            else:
                raise ValueError(f"Unsupported goruut architecture or version: {version}")
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                self.executable_path = self.executable.exists(temp_dir)
            except Exception as e:
                self.executable_path = self.executable.download(temp_dir)
            self.config = Config()
            self.config.serialize(os.path.join(temp_dir, "goruut_config.json"))
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
                    
    def exact_version(self) -> str:
        return self.version

    def compatible_version(self) -> str:
        return self.version.rstrip('0123456789')
    
    def __del__(self):
        if hasattr(self, 'process'):
            self.process.terminate()
            self.process.wait()

    def phonemize(self, language="Greek", sentence="Σήμερα...") -> PhonemeResponse:
        # handle ISO here
        language = PygoruutLanguages()[language]
        url = self.config.url("tts/phonemize/sentence")
        payload = {"Language": language, "Sentence": sentence}
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        data = response.json()
        words = [Word(**word) for word in data["Words"]]
        return PhonemeResponse(Words=words)
