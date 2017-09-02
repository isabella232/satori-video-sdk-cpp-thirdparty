from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class SdlConan(ConanFile):
    name = "SDL"
    version = "2.0.5"
    license = "zlib"
    url = "https://www.libsdl.org/index.php"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=False"
    folder_name = "SDL2-%s" % version

    def source(self):
        zip_name = "%s.tar.gz" % self.folder_name
        url = "https://libsdl.org/release/%s" % zip_name
        self.output.info("Downloading %s" % url)
        tools.download(url, zip_name)
        tools.unzip(zip_name, ".")
        os.unlink(zip_name)

    def build(self):
        configure_args = []

        prefix = os.path.abspath("install")
        configure_args.append("--prefix=%s" % prefix)
        configure_args.append(
            "--enable-shared" if self.options.shared else "--disable-shared")
        configure_args.append(
            "--disable-static" if self.options.shared else "--enable-static")
        if self.options.fPIC:
            configure_args.append("--with-pic")

        env_build = AutoToolsBuildEnvironment(self)
        env_vars = dict(env_build.vars)
        with tools.environment_append(env_vars):
            self.output.info("Build environment: %s" % env_vars)
            self.output.info("config %s" % " ".join(configure_args))
            self.run("cd %s && ./configure -v %s" %
                     (self.folder_name, " ".join(configure_args)))
            self.run("cd %s && make all -j%s" %
                     (self.folder_name, tools.cpu_count()))
            self.run("cd %s && make install" %
                     self.folder_name)

    def package(self):
        self.copy("*", src="install")

    def package_info(self):
        self.cpp_info.libs = ["SDL2"]
