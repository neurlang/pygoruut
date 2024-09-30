import os
import stat
import hashlib
import requests
from dataclasses import dataclass
from pygoruut.goplatform import Architecture, OS, Platform
from pygoruut.releases import releases
from typing import List

@dataclass
class Executable:
    size: int
    sha256: str
    architecture: Architecture
    os: OS
    servers: List[str]

    def __post_init__(self):
        if not isinstance(self.size, int) or self.size <= 0:
            raise ValueError("Size must be a positive integer")
        
        if not isinstance(self.sha256, str) or len(self.sha256) != 64:
            raise ValueError("SHA256 must be a 64-character string")
        
        if not isinstance(self.architecture, Architecture):
            raise ValueError("Architecture must be an instance of Architecture enum")
        
        if not isinstance(self.os, OS):
            raise ValueError("OS must be an instance of OS enum")
            
        if not isinstance(self.servers, List) or len(self.servers) <= 0:
            raise ValueError("servers must exist")
    
    @property
    def file_name(self) -> str:
        base_name = "goruut"
        arch = self._transform_arch()
        os_ext = self._transform_os_ext()
        return f"{base_name}.{self.sha256}.{arch}.{self.os.value}{os_ext}"

    @property
    def file_name_public(self) -> str:
        base_name = "goruut"
        arch = self._transform_arch()
        os_ext = self._transform_os()
        return f"{base_name}-{self.os.value}-{arch}"

    def _transform_arch(self) -> str:
        return self.architecture.value
    
    def _transform_os(self) -> str:
        return self.os.value

    def _transform_os_ext(self) -> str:
        if self.os == OS.WINDOWS:
            return ".exe"
        elif self.os == OS.LINUX:
            return ".bin"
        elif self.os == OS.DARWIN:
            return ".dmg"
        else:
            return ""  # For other OS types, no specific extension

    def exists(self, temp_dir: str) -> str:
        temp_file_path = os.path.join(temp_dir, self.file_name)
        try:
            # Verify file size
            if os.path.getsize(temp_file_path) != self.size:
                raise ValueError(f"Preexisting file size does not match expected size")
            
            # Verify SHA256
            sha256_hash = hashlib.sha256()
            with open(temp_file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            if sha256_hash.hexdigest() != self.sha256:
                raise ValueError("SHA256 hash of preexisting file does not match expected hash")
            # If we've made it here, all checks have passed
            return temp_file_path
        
        except Exception as e:
            # If anything goes wrong, delete the temp file if it exists
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            raise RuntimeError(f"Failed to verify preexisting executable: {str(e)}")
            
    def download(self, temp_dir: str) -> str:
        temp_file_path = os.path.join(temp_dir, self.file_name)
        
        try:
          exception = ValueError(f"Downloaded file doesn't have any server to load from")
          
          for url_prefix in self.servers:
            url = f"{url_prefix}{self.file_name_public}"
        
            # Download the file
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(temp_file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Verify file size
            if os.path.getsize(temp_file_path) != self.size:
                exception = ValueError(f"Downloaded file size does not match expected size")
            
            # Verify SHA256
            sha256_hash = hashlib.sha256()
            with open(temp_file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            if sha256_hash.hexdigest() != self.sha256:
                exception = ValueError("SHA256 hash of downloaded file does not match expected hash")
            
            # Get the current file permissions
            st = os.stat(temp_file_path)
    
            # Add executable permission for the user, group, and others
            os.chmod(temp_file_path, st.st_mode | stat.S_IEXEC)
            
            # If we've made it here, all checks have passed
            return temp_file_path
            
          # If we've made it here, there is some exception
          raise exception

        except Exception as e:
            # If anything goes wrong, delete the temp file if it exists
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            raise RuntimeError(f"Failed to download and verify executable: {str(e)}")

    def __str__(self):
        return (f"Executable(file_name: {self.file_name}, "
                f"size: {self.size} bytes, "
                f"sha256: {self.sha256[:6]}...{self.sha256[-6:]}, "
                f"architecture: {self.architecture.value}, "
                f"os: {self.os.value})")



@dataclass
class MyPlatformExecutable:
    def __init__(self, version=None):
      self.myplatf = Platform()
      self.version = version
      self.exe = None

      for release in releases:
        if self.version is not None and not release[1].startswith(self.version):
          continue
        
        platf = Platform(release[4], release[5])
        if str(platf) != str(self.myplatf):
          continue
        
        self.exe = Executable(
            size=release[2],
            sha256=release[3],
            architecture=Architecture(release[4]),
            os=OS(release[5]),
            servers=release[6],
        )
        self.version = release[1]
        break
    
    def get(self):
        return self.exe, self.myplatf, self.version

# Example usage
if __name__ == "__main__":
    from goplatform import Architecture, OS, Platform
    import tempfile
    from releases import releases
    
    try:
    
      myarch = Platform()
    
      for release in releases:
    
        exe = Executable(
            size=release[2],
            sha256=release[3],
            architecture=Architecture(release[4]),
            os=OS(release[5]),
            servers=release[6],
        )
        print(exe)

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                downloaded_path = exe.download(temp_dir)
                print(f"Successfully downloaded and verified: {downloaded_path}")
            except RuntimeError as e:
                print(f"Download failed: {e}")

    except ValueError as e:
        print(f"Error creating Executable: {e}")
