from conans import ConanFile, CMake, RunEnvironment, tools
import os

class LibcborTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    options = {"shared": [True, False],
               "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=False"

    def build(self):
        self.output.info("conan options: %s" % self.options.values)
        self.output.info("conan settings: %s" % self.settings.values_list)

        cmake = CMake(self)
        cmake.configure(source_dir=self.conanfile_directory, build_dir="./", defs={
            "CMAKE_VERBOSE_MAKEFILE": "ON"
        })
        cmake.build()

    def imports(self):
        self.copy("libcbor-test", dst="bin")

    def test(self):
        env_build = RunEnvironment(self)
        print env_build.vars
        with tools.environment_append(env_build.vars):
            self.run("./bin/libcbor-test")
