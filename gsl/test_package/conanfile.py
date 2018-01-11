from conans import ConanFile, CMake
import os


class GslTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is
        # in "test_package"
        cmake.configure(build_dir="./")
        cmake.build()

    def test(self):
        os.chdir("bin")
        self.run("./test")
