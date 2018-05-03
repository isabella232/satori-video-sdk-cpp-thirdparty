from conans import ConanFile, CMake, tools


class GoogletestConan(ConanFile):
    name = "Googletest"
    version = "1.8.0-40"
    license = "BSD 3"
    url = "https://github.com/google/googletest"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=False"
    generators = "cmake"

    def source(self):
        self.run("git clone -b release-%s https://github.com/google/googletest" % self.version)

    def build(self):
        cmake = CMake(self)

        cmake_options = []
        cmake_options.append("-GNinja")
        cmake_options.append("-DCMAKE_VERBOSE_MAKEFILE=ON")
        cmake_options.append("-DCMAKE_BUILD_TYPE=%s" %
                             self.settings.build_type)
        cmake_options.append("-DBUILD_SHARED_LIBS=%s" %
                             ("ON" if self.options.shared else "OFF"))
        ## cmake_options.append("-DCMAKE_INSTALL_PREFIX=install")
        if self.options.fPIC:
            if "CFLAGS" in os.environ:
                cmake_options.append("-DCMAKE_C_FLAGS=\"-fPIC %s\"" % os.environ["CFLAGS"])
            if "CXXFLAGS" in os.environ:
                cmake_options.append("-DCMAKE_CXX_FLAGS=\"-fPIC %s\"" % os.environ["CXXFLAGS"])
        else:
            if "CFLAGS" in os.environ:
                cmake_options.append("-DCMAKE_C_FLAGS=\"%s\"" % os.environ["CFLAGS"])
            if "CXXFLAGS" in os.environ:
                cmake_options.append("-DCMAKE_CXX_FLAGS=\"%s\"" % os.environ["CXXFLAGS"])

        cmake_command = ('cmake googletest %s %s' %
                         (cmake.command_line, " ".join(cmake_options)))
        self.output.info(cmake_command)
        self.run(cmake_command)
        self.run("cmake --build . %s --target install" % cmake.build_config)

    def package_info(self):
        self.cpp_info.libs = ["gtest"]
