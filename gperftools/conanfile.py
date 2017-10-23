from conans import ConanFile, AutoToolsBuildEnvironment, tools

import os


class GperftoolsConan(ConanFile):
    name = "GPerfTools"
    version = "2017.10.16"
    tag = "6e3a702fb9c86eb450f22b326ecbceef4b0d6604"
    license = "BSD-3-Clause"
    url = "https://github.com/gperftools/gperftools"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=False"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/gperftools/gperftools.git")
        self.run("cd gperftools && git checkout %s" % self.tag)

    def build(self):
        configure_args = []

        prefix = os.path.abspath("install")
        configure_args.append("--prefix=%s" % prefix)

        configure_args.append("--enable-shared=%s" %
                              ("yes" if self.options.shared else "no"))
        configure_args.append("--enable-static=%s" %
                              ("yes" if not self.options.shared else "no"))

        if self.options.fPIC:
            configure_args.append("--with-pic")

        env_build = AutoToolsBuildEnvironment(self)
        env_vars = dict(env_build.vars)
        with tools.environment_append(env_vars):
            self.output.info("Build environment: %s" % env_vars)
            self.run("cd gperftools && ./autogen.sh")
            self.output.info("./configure %s" % " ".join(configure_args))
            self.run("cd gperftools && ./configure %s" %
                     " ".join(configure_args))
            self.run("cd gperftools && make -j 8")
            self.run("cd gperftools && make -j 8 install")

    def package(self):
        self.copy("*", src="install")

    def package_info(self):
        if self.options.shared:
            self.cpp_info.libs = ["tcmalloc", "profiler"]
        else:
            self.cpp_info.libs = ["tcmalloc_and_profiler"]
            
        self.cpp_info.libs.append("pthread")

        if self.settings.compiler == "gcc":
            self.cpp_info.cflags = [
                "-fno-builtin-malloc", "-fno-builtin-calloc", "-fno-builtin-realloc", "-fno-builtin-free"]
            self.cpp_info.cppflags = [
                "-fno-builtin-malloc", "-fno-builtin-calloc", "-fno-builtin-realloc", "-fno-builtin-free"]
