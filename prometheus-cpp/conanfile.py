from conans import ConanFile, CMake
import os


class PrometheuscppConan(ConanFile):
    name = "PrometheusCpp"
    version = "2018.04.23"
    tag = "73ac260f489300dc54d743e595d310de7eb255fa"
    license = "MIT"
    url = "https://github.com/jupp0r/prometheus-cpp"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=False"
    generators = "cmake"


    def source(self):
        self.run("git clone --recursive https://github.com/jupp0r/prometheus-cpp.git")
        self.run("cd prometheus-cpp && git checkout %s" % self.tag)


    def build(self):
        if self.options.shared:
            raise Exception("Shared build not supported")

        cmake = CMake(self)

        cmake_options = []
        cmake_options.append("-GNinja")
        cmake_options.append("-DCMAKE_VERBOSE_MAKEFILE=ON")
        cmake_options.append("-DCMAKE_BUILD_TYPE=%s" %
                             self.settings.build_type)
        cmake_options.append("-DCMAKE_INSTALL_PREFIX=install")
        if self.options.fPIC:
            cmake_options.append("-DCMAKE_C_FLAGS=-fPIC")
            cmake_options.append("-DCMAKE_CXX_FLAGS=-fPIC")

        cmake_command = ('cmake prometheus-cpp %s %s' %
                         (cmake.command_line, " ".join(cmake_options)))
        self.output.info(cmake_command)
        self.run(cmake_command)
        self.run("cmake --build . %s --target install" % cmake.build_config)


    def package(self):
        self.copy("*", dst="include", src="prometheus-cpp/include")

        if self.options.shared:
            self.copy("*prometheus*.dll", dst="bin", keep_path=False)
            self.copy("*prometheus*.so", dst="lib", keep_path=False)
            self.copy("*prometheus*.dylib", dst="lib", keep_path=False)

        if not self.options.shared:
            self.copy("*prometheus*.a", dst="lib", keep_path=False)


    def package_info(self):
        self.cpp_info.libs = ["prometheus-cpp"]
