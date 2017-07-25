from conans import ConanFile, tools
import os
import sys


class BoostConan(ConanFile):
    name = "Boost"
    version = "1.64.0"
    license = "Boost Software License"
    url = "http://www.boost.org/"
    settings = "os", "compiler", "build_type", "arch"
    description = "boost software library"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_program_options": [True, False],
        "with_system": [True, False],
        "with_regex": [True, False]}
    default_options = "shared=False", \
        "fPIC=False", \
        "with_program_options=True", \
        "with_system=True", \
        "with_regex=True"
    FOLDER_NAME = "boost_%s" % version.replace(".", "_")

    def source(self):
        zip_name = "%s.zip" % self.FOLDER_NAME if sys.platform == "win32" else "%s.tar.gz" % self.FOLDER_NAME
        url = "http://sourceforge.net/projects/boost/files/boost/%s/%s/download" % (
            self.version, zip_name)
        self.output.info("Downloading %s" % url)
        tools.download(url, zip_name)
        tools.unzip(zip_name, ".")
        os.unlink(zip_name)

    def bootstrap(self):
        command = "bootstrap" if self.settings.os == "Windows" else "./bootstrap.sh"
        flags = []
        flags.append("link=%s" %
                     ("static" if not self.options.shared else "shared"))
        flags.append("address-model=%s" %
                     ("32" if self.settings.arch == "x86" else "64"))

        libraries = []
        if (self.options.with_program_options):
            libraries.append("program_options")
        if (self.options.with_system):
            libraries.append("system")
        if (self.options.with_regex):
            libraries.append("regex")
        flags.append("--with-libraries=%s" % ",".join(libraries))

        self.output.info("Boostrapping %s %s" % (self.FOLDER_NAME, flags))

        self.run("cd %s && %s %s" %
                 (self.FOLDER_NAME, command, " ".join(flags)))

    def build(self):
        self.bootstrap()
        self.output.info("Building %s" % (self.FOLDER_NAME))

        flags = []
        cxx_flags = []
        if self.options.fPIC:
            cxx_flags.append("-fPIC")
        cxx_flags = 'cxxflags="%s"' % " ".join(cxx_flags) if cxx_flags else ""
        flags.append(cxx_flags)

        self.run("cd %s && ./b2 %s -j%s" %
                 (self.FOLDER_NAME, " ".join(flags), tools.cpu_count()))

    def package(self):
        self.copy(pattern="*", dst="include/boost",
                  src="%s/boost" % self.FOLDER_NAME)
        if self.options.shared:
            self.copy(pattern="*.so", dst="lib", src="%s/stage/lib" %
                      self.FOLDER_NAME)
            self.copy(pattern="*.so.*", dst="lib",
                      src="%s/stage/lib" % self.FOLDER_NAME)
            self.copy(pattern="*.dylib*", dst="lib",
                      src="%s/stage/lib" % self.FOLDER_NAME)
            self.copy(pattern="*.dll", dst="bin",
                      src="%s/stage/lib" % self.FOLDER_NAME)
        else:
            self.copy(pattern="*.a", dst="lib", src="%s/stage/lib" %
                      self.FOLDER_NAME)
            self.copy(pattern="*.lib", dst="lib",
                      src="%s/stage/lib" % self.FOLDER_NAME)
                      src="%s/stage/lib" % self.FOLDER_NAME)
        pass

    def package_info(self):
        libs = []
        if (self.options.with_program_options):
            libs.append("boost_program_options")
        if (self.options.with_system):
            libs.append("boost_system")
        if (self.options.with_regex):
            libs.append("boost_regex")
        self.cpp_info.libs = libs
