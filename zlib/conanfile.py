from conans import ConanFile, CMake


class ZlibConan(ConanFile):
    name = "Zlib"
    version = "v1.2.11"
    license = "BSD-like"
    url = "http://zlib.net/"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=False"
    generators = "cmake"

    def source(self):
        self.run("git clone -b %s https://github.com/madler/zlib" % self.version)

    def build(self):
        cmake = CMake(self)

        cmake_options = []
        cmake_options.append("-GNinja")
        cmake_options.append("-DCMAKE_VERBOSE_MAKEFILE=ON")
        cmake_options.append("-DCMAKE_BUILD_TYPE=%s" %
                             self.settings.build_type)
        cmake_options.append("-DBUILD_SHARED_LIBS=%s" %
                             ("ON" if self.options.shared else "OFF"))
        if self.options.fPIC:
            cmake_options.append("-DCMAKE_C_FLAGS=-fPIC")
            cmake_options.append("-DCMAKE_CXX_FLAGS=-fPIC")

        cmake_command = ('cmake zlib %s %s' %
                         (cmake.command_line, " ".join(cmake_options)))
        self.output.info(cmake_command)
        self.run(cmake_command)
        self.run("cmake --build . %s --target install" % cmake.build_config)

    def package_info(self):
        self.cpp_info.libs = ["z"]