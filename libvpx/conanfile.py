from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class LibvpxConan(ConanFile):
    name = "Libvpx"
    version = "1.6.1-40"
    source_version = "1.6.1"
    license = "custom"
    url = "https://chromium.googlesource.com/webm/libvpx"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [
        True, False], "emcc": [True, False]}
    default_options = "shared=False", "fPIC=False", "emcc=False"

    def source(self):
        self.run(
            "git clone --depth 1 -b v%s https://chromium.googlesource.com/webm/libvpx" % (self.source_version))

    def build(self):
        configure_args = []

        prefix = os.path.abspath("install")
        configure_args.append("--prefix=%s" % prefix)
        if self.options.fPIC:
            configure_args.append("--enable-pic")
        if self.options.shared:
            configure_args.append("--enable-shared")
        if self.settings.build_type == "Debug":
            configure_args.append("--enable-debug")

        # disable features and parts
        configure_args.append("--disable-examples")
        configure_args.append("--disable-tools")
        configure_args.append("--disable-docs")
        configure_args.append("--disable-unit-tests")

        if self.options.emcc:
            if not self.options.shared:
                raise Exception(
                    "emcc should be used with shared libraries only.")
            configure_args.append("--target=generic-gnu")
            configure_args.append("--disable-static")
            configure_args.append("--enable-shared")
            configure_args.append("--disable-multithread")

        if self.settings.build_type == "Debug":
            configure_args.append("--enable-debug")

        env_build = AutoToolsBuildEnvironment(self)
        env_vars = dict(env_build.vars)
        # env_vars["KERNEL_BITS"] = "64"
        with tools.environment_append(env_vars):
            self.output.info("Build environment: %s" % env_vars)
            self.output.info("config %s" % " ".join(configure_args))
            self.run("cd libvpx && ./configure %s" %
                     " ".join(configure_args))
            self.run("cd libvpx && V=1 make -j%s all install" %
                     tools.cpu_count())

    def package(self):
        self.copy("*", src="install")

    def package_info(self):
        self.cpp_info.libs = ["vpx"]
