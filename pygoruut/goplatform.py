import enum
import platform
import sys

class Architecture(enum.Enum):
    AMD64 = "amd64"
    ARM = "arm"
    ARM64 = "arm64"

class OS(enum.Enum):
    ANDROID = "android"
    DARWIN = "darwin"
    LINUX = "linux"
    WINDOWS = "windows"

class Platform:
    def __init__(self, arch=None, os=None):
        self.architecture = Architecture(arch) if arch is not None else self._determine_architecture()
        self.os = OS(os) if os is not None else self._determine_os()

    def _determine_architecture(self):
        machine = platform.machine().lower()
        if machine in ('x86_64', 'amd64'):
            return Architecture.AMD64
        elif machine.startswith('arm'):
            if '64' in machine:
                return Architecture.ARM64
            else:
                return Architecture.ARM
        else:
            raise ValueError(f"Unsupported architecture: {machine}")

    def _determine_os(self):
        system = platform.system().lower()
        if system == 'linux':
            # Check if it's Android
            if hasattr(sys, 'getandroidapilevel'):
                return OS.ANDROID
            return OS.LINUX
        elif system == 'darwin':
            return OS.DARWIN
        elif system == 'windows':
            return OS.WINDOWS
        else:
            raise ValueError(f"Unsupported OS: {system}")

    def __str__(self):
        return f"Platform(OS: {self.os.value}, Architecture: {self.architecture.value})"

# Example usage
if __name__ == "__main__":
    platform = Platform()
    print(platform)
