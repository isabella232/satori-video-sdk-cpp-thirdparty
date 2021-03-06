from conans import ConanFile, CMake
import os


class BeastTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_dir="./")
        cmake.build()

    def test(self):
        os.chdir("bin")
        self.run("./test")
