from conans import ConanFile, CMake, tools
import os


class SdlConan(ConanFile):
    name = "SDL"
    version = "2.0.5-40"
    source_version = "2.0.5"
    license = "zlib"
    url = "https://www.libsdl.org/index.php"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=False"
    folder_name = "SDL2-%s" % source_version

    def source(self):
        zip_name = "%s.tar.gz" % self.folder_name
        url = "https://libsdl.org/release/%s" % zip_name
        self.output.info("Downloading %s" % url)
        tools.download(url, zip_name)
        tools.unzip(zip_name, ".")
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self)

        cmake_options = []
        cmake_options.append("-GNinja")
        cmake_options.append("-DCMAKE_VERBOSE_MAKEFILE=ON")
        cmake_options.append("-DCMAKE_BUILD_TYPE=%s" %
                             self.settings.build_type)
        cmake_options.append("-DBUILD_SHARED_LIBS=%s" %
                             ("ON" if self.options.shared else "OFF"))
        cmake_options.append("-DSDL_SHARED_ENABLED_BY_DEFAULT=%s" %
                             ("ON" if self.options.shared else "OFF"))
        cmake_options.append("-DCMAKE_INSTALL_PREFIX=install")
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

        cmake_command = ('cmake %s %s %s' %
                         (self.folder_name, cmake.command_line, " ".join(cmake_options)))
        self.output.info(cmake_command)
        self.run(cmake_command)
        self.run("cmake --build . %s --target install" % cmake.build_config)

    def package(self):
        self.copy("*", src="install")

    def package_info(self):
        self.cpp_info.libs = ["SDL2", "pthread", "dl"]

        if self.settings.os == "Macos":
            self.cpp_info.libs.append("iconv")
            self.cpp_info.exelinkflags.append("-framework AppKit")
            self.cpp_info.exelinkflags.append("-framework AudioToolbox")
            self.cpp_info.exelinkflags.append("-framework Carbon")
            self.cpp_info.exelinkflags.append("-framework CoreAudio")
            self.cpp_info.exelinkflags.append("-framework CoreVideo")
            self.cpp_info.exelinkflags.append("-framework ForceFeedback")
            self.cpp_info.exelinkflags.append("-framework IOKit")
