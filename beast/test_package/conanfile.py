from conans import ConanFile, CMake
import os


class BeastTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    options = {"fPIC": [True, False]}
    default_options = "fPIC=False"

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir=self.conanfile_directory, build_dir="./")
        cmake.build()

    def test(self):
        os.chdir("bin")
        self.run("./test")
