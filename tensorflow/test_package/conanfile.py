from conans import ConanFile, CMake
import os


class TensorflowTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_dir="./")
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")

    def test(self):
        os.chdir("bin")

        if self.settings.os == "Macos":
            # https://stackoverflow.com/questions/35568122/why-isnt-dyld-library-path-being-propagated-here
            self.run("DYLD_LIBRARY_PATH=%s  ./example" %
                     os.environ['DYLD_LIBRARY_PATH'])
        else:
            self.run(".%sexample" % os.sep)
