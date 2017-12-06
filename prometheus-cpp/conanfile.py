from conans import ConanFile, CMake, tools
import os


class PrometheuscppConan(ConanFile):
    name = "PrometheusCpp"
    version = "2017.12.06"
    license = "<Put the package license here>"
    url = "https://github.com/jupp0r/prometheus-cpp"
    tag = "b9906b514baa1ac21f7e13b4271ad9c36be0b170"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=False"
    generators = "cmake"
    requires = "Protobuf/3.4.1@satorivideo/master"

    def requirements(self):
        self.options["Protobuf"].shared = self.options.shared
        self.options["Protobuf"].fPIC = self.options.fPIC

    def source(self):
        self.run("git clone --recursive https://github.com/jupp0r/prometheus-cpp.git")
        self.run("cd prometheus-cpp && git checkout %s" % self.tag)

    def build(self):
        if self.options.shared:
            raise Exception("Shared build not supported")

        cmake = CMake(self)

        cmake.definitions["CMAKE_LIBRARY_PATH"] = os.path.join(
            self.deps_cpp_info["Protobuf"].rootpath,
            self.deps_cpp_info["Protobuf"].libdirs[0])

        cmake.definitions["Protobuf_INCLUDE_DIR"] = os.path.join(
            self.deps_cpp_info["Protobuf"].rootpath,
            self.deps_cpp_info["Protobuf"].includedirs[0])

        cmake.definitions["Protobuf_LIBRARIES"] = os.path.join(
            self.deps_cpp_info["Protobuf"].rootpath,
            self.deps_cpp_info["Protobuf"].libdirs[0],
            "libprotobuf.a")

        cmake.definitions["Protobuf_PROTOC_EXECUTABLE"] = os.path.join(
            self.deps_cpp_info["Protobuf"].rootpath,
            self.deps_cpp_info["Protobuf"].bindirs[0],
            "protoc")

        self.output.warn("Configuring: cmake %s" % cmake.command_line)
        cmake.configure(source_dir="prometheus-cpp", build_dir="./")
        cmake.build()

    def package(self):
        self.copy("*", dst="include", src="prometheus-cpp/include")
        self.copy("*.h", dst="include",
                  src="lib/cpp/")

        if self.options.shared:
            self.copy("*prometheus*.dll", dst="bin", keep_path=False)
            self.copy("*prometheus*.so", dst="lib", keep_path=False)
            self.copy("*prometheus*.dylib", dst="lib", keep_path=False)

        if not self.options.shared:
            self.copy("*prometheus*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["prometheus-cpp"]
