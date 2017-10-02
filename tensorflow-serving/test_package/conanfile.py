from conans import ConanFile, CMake
import os


class TensorflowservingTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir=self.conanfile_directory, build_dir="./")
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")

    def test(self):
        self.output.info("*** test environment: %s" % os.environ)
        os.chdir("bin")
        self.run(".%sexample" % os.sep)
