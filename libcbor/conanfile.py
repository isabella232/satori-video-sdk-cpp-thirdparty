import os
from conans import ConanFile, CMake, tools


class LibcborConan(ConanFile):
    name = "Libcbor"
    version = "0.5.0-40"
    license = "MIT"
    url = "https://github.com/PJK/libcbor"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=False"
    generators = "cmake"

    def source(self):
        self.run(
            "git clone --depth 1 --branch v%s https://github.com/PJK/libcbor.git" % self.version)
        tools.replace_in_file("libcbor/CMakeLists.txt", "-flto", "")

    def build(self):
        cmake = CMake(self)

        cmake_options = []
        cmake_options.append("-DCMAKE_VERBOSE_MAKEFILE=ON")
        cmake_options.append("-DCMAKE_BUILD_TYPE=%s" %
                             self.settings.build_type)
        cmake_options.append("-DBUILD_SHARED_LIBS=%s" %
                             ("ON" if self.options.shared else "OFF"))
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

        cmake_command = ('cmake libcbor %s %s' %
                         (cmake.command_line, " ".join(cmake_options)))
        self.output.info(cmake_command)
        self.run(cmake_command)
        self.run("cmake --build . %s --target cbor" % cmake.build_config)
        if self.options.shared:
            self.run("cmake --build . %s --target cbor_shared" %
                     cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="libcbor/src")
        self.copy("*.h", dst="include/cbor", src="cbor")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.so.*", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["cbor"]
