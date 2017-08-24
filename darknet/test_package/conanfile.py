from conans import ConanFile, CMake, RunEnvironment, tools
import os

channel = os.getenv("CONAN_CHANNEL", "master")
username = os.getenv("CONAN_USERNAME", "satorivideo")


class LibcborTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "Darknet/0.1.1@%s/%s" % (username, channel)
    generators = "cmake"
    options = {"shared": [True, False],
               "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=False"

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir=self.conanfile_directory, build_dir="./", defs={
            "CMAKE_VERBOSE_MAKEFILE": "ON"
        })
        cmake.build()

    def imports(self):
        self.copy("darknet-test", dst="bin")

    def test(self):
        env_build = RunEnvironment(self)
        print env_build.vars
        with tools.environment_append(env_build.vars):
            self.run("./bin/darknet-test")
