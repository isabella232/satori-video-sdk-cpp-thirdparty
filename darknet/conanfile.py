from conans import ConanFile, CMake, tools


class DarknetConan(ConanFile):
    name = "Darknet"
    version = "0.1.0"
    # this packet has no releases, it is known stable commit
    revision = "7a223d8591e0a497889b9fce9bc43ac4bd3969fd"
    license = "MIT"
    url = "https://github.com/pjreddie/darknet"
    settings = "os", "compiler", "build_type", "arch"

    def source(self):
        self.run(
            "git clone https://github.com/pjreddie/darknet && cd darknet && git checkout %s" % self.revision)
        if self.settings.os == "Macos":
            tools.replace_in_file("darknet/src/utils.c", "clock_gettime(CLOCK_REALTIME, &now)", "")
        else:
            tools.replace_in_file("darknet/Makefile", "OPENMP=0", "OPENMP=1")

    def build(self):
        self.run("make -C darknet")

    def package(self):
        self.copy("*.h", dst="include", src="darknet/include")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.so.*", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["darknet"]
