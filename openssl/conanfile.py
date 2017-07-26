from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class OpensslConan(ConanFile):
    name = "Openssl"
    version = "1.1.0f"
    license = "OpenSSL License"
    url = "https://www.openssl.org/"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=False"
    generators = "cmake"
    folder_name = "openssl-%s" % version

    def source(self):
        zip_name = "%s.tar.gz" % self.folder_name
        url = "https://www.openssl.org/source/%s" % zip_name
        self.output.info("Downloading %s" % url)
        tools.download(url, zip_name)
        tools.unzip(zip_name, ".")
        os.unlink(zip_name)

    def build(self):
        configure_args = []

        prefix = os.path.abspath("install")
        configure_args.append("--prefix=%s" % prefix)
        configure_args.append("pic" if self.options.fPIC else "no-pic")
        configure_args.append("shared" if self.options.shared else "no-shared")

        env_build = AutoToolsBuildEnvironment(self)
        env_vars = dict(env_build.vars)
        env_vars["KERNEL_BITS"] = "64"
        with tools.environment_append(env_vars):
            self.output.info("Build environment: %s" % env_vars)
            self.output.info("config %s" % " ".join(configure_args))
            self.run("cd %s && ./config %s" %
                     (self.folder_name, " ".join(configure_args)))
            self.run("cd %s && make depend -j%s" %
                     (self.folder_name, tools.cpu_count()))
            self.run("cd %s && make all -j%s" %
                     (self.folder_name, tools.cpu_count()))
            self.run("cd %s && make install_sw" %
                     self.folder_name)

    def package(self):
        self.copy("*", src="install")

    def package_info(self):
        self.cpp_info.libs = ["ssl", "crypto"]
