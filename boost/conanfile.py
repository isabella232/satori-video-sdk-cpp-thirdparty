from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os
import sys

USER_CONFIG_JAM = """
using {toolset} : : {cxx} ;
"""


class BoostConan(ConanFile):
    name = "Boost"
    version = "1.66.0-01"
    tag = "1.66.0"
    license = "Boost Software License"
    url = "http://www.boost.org/"
    settings = "os", "compiler", "build_type", "arch"
    description = "boost software library"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_program_options": [True, False],
        "with_system": [True, False],
        "with_regex": [True, False],
        "with_timer": [True, False]}
    default_options = "shared=False", \
        "fPIC=False", \
        "with_program_options=True", \
        "with_system=True", \
        "with_regex=True", \
        "with_timer=True"
    FOLDER_NAME = "boost_%s" % tag.replace(".", "_")

    def source(self):
        zip_name = "%s.zip" % self.FOLDER_NAME if sys.platform == "win32" else "%s.tar.gz" % self.FOLDER_NAME
        url = "http://sourceforge.net/projects/boost/files/boost/%s/%s/download" % (
            self.tag, zip_name)
        self.output.info("Downloading %s" % url)
        tools.download(url, zip_name)
        tools.unzip(zip_name, ".")
        os.unlink(zip_name)

    def bootstrap(self):
        boostrap_command = "bootstrap" if self.settings.os == "Windows" else "./bootstrap.sh"
        build_folder = "%s/tools/build" % (self.FOLDER_NAME)
        b2_path = os.path.abspath(os.curdir)

        self.output.info("Boostrapping Boost.Build")
        self.run("cd %s && %s" % (build_folder, boostrap_command))
        self.output.info("Building Boost.Build")
        self.run("cd %s && %s" %
                 (build_folder, "./b2 install --prefix=%s/b2" % b2_path))

    def toolset(self):
        if self.settings.os == "Linux":
            if "clang" in self.settings.compiler:
                return "clang"
            else:
                return self.settings.compiler

    def build(self):
        self.bootstrap()
        flags = []

        libraries = []
        if self.options.with_program_options:
            libraries.append("program_options")
        if self.options.with_system:
            libraries.append("system")
        if self.options.with_regex:
            libraries.append("regex")
        if self.options.with_timer:
            libraries.append("timer")
        flags.extend(["--with-%s" % lib for lib in libraries])

        toolset = self.toolset()
        flags.append("toolset=%s" % toolset)
        if "CXX" in os.environ:
            tools.save("%s/tools/build/src/user-config.jam" %
                       self.FOLDER_NAME, USER_CONFIG_JAM.format(
                           toolset=toolset,
                           cxx=os.environ["CXX"]
                       ))

        flags.append("link=%s" %
                     ("static" if not self.options.shared else "shared"))
        flags.append("address-model=%s" %
                     ("32" if self.settings.arch == "x86" else "64"))

        env_build = AutoToolsBuildEnvironment(self)
        env_vars = dict(env_build.vars)
        self.output.info("build env: %s" % env_vars)

        cxxflags = [env_vars["CXXFLAGS"]]
        if self.options.fPIC:
            cxxflags.append("-fPIC")
        flags.append('cxxflags="%s"' % " ".join(cxxflags))

        cflags = [env_vars["CFLAGS"]]
        if self.options.fPIC:
            cflags.append("-fPIC")
        flags.append('cflags="%s"' % " ".join(cflags))

        ldflags = [env_vars["LDFLAGS"]]
        flags.append('linkflags="%s"' % " ".join(ldflags))

        self.output.info("Building %s %s" % (self.FOLDER_NAME, flags))
        self.run("cd %s && ../b2/bin/b2 %s -j%s stage" %
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

    def package_info(self):
        libs = []
        if self.options.with_program_options:
            libs.append("boost_program_options")
        if self.options.with_system:
            libs.append("boost_system")
        if self.options.with_regex:
            libs.append("boost_regex")
        if self.options.with_timer:
            libs.append("boost_timer")
            libs.append("boost_chrono")
        self.cpp_info.libs = libs
