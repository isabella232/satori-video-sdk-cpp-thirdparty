from conans import ConanFile, CMake


class LibcborConan(ConanFile):
    name = "Libcbor"
    version = "0.5.0"
    license = "MIT"
    url = "https://github.com/PJK/libcbor"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "fPIC": [True, False]}
    default_options = "shared=True", "fPIC=False"
    generators = "cmake"

    def source(self):
        self.run(
            "git clone --depth 1 --branch v%s https://github.com/PJK/libcbor.git" % self.version)
        self.run("cd libcbor")

    def build(self):
        cmake = CMake(self)

        cmake_options = []
        if self.options.shared:
            cmake_options.append("-DBUILD_SHARED_LIBS=ON")
        if self.options.fPIC:
            cmake_options.append("-DCMAKE_C_FLAGS=-fPIC")

        self.run('cmake -DCMAKE_VERBOSE_MAKEFILE=ON libcbor %s %s' %
                 (cmake.command_line, " ".join(cmake_options)))
        self.run("cmake --build . %s --target cbor" % cmake.build_config)
        if self.options.shared:
            self.run("cmake --build . %s --target cbor_shared" %
                     cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="libcbor/src")
        self.copy("*.h", dst="include/cbor", src="cbor")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.so.*", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["cbor"]
