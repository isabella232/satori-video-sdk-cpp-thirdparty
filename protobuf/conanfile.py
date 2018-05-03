from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class ProtobufConan(ConanFile):
    name = "Protobuf"
    version = "3.4.1-40"
    license = "<Put the package license here>"
    url = "https://github.com/google/protobuf.git"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=False"
    generators = "cmake"

    def source(self):
        self.run(
            "git clone  --depth 1 -b v%s https://github.com/google/protobuf.git" % self.version)

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
            self.run("cd protobuf && ./autogen.sh")
            self.output.info("./configure %s" % " ".join(configure_args))
            self.run("cd protobuf && ./configure %s" %
                     " ".join(configure_args))
            self.run("cd protobuf && make -j%s" % tools.cpu_count())
            self.run("cd protobuf && make install")

    def package(self):
        self.copy("*", src="install")

    def package_info(self):
        self.cpp_info.libs = ["protobuf"]
