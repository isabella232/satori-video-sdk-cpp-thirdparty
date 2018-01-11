from conans import ConanFile, CMake
import os

class SdlTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    options = {"fPIC": [True, False], "shared": [True, False]}
    default_options = "fPIC=False", "shared=False"

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_dir="./")
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")

    def test(self):
        os.chdir("bin")
        self.run(".%sexample" % os.sep)
