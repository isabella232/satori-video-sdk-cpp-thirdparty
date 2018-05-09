from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os

FPIC_PATCH = """
diff --git a/Makefile b/Makefile
index 9754ddf..4c735c3 100644
--- a/Makefile
+++ b/Makefile
@@ -24 +24 @@ BIGFILES=-D_FILE_OFFSET_BITS=64
-CFLAGS=-Wall -Winline -O2 -g $(BIGFILES)
+CFLAGS=-Wall -Winline -O2 -g $(BIGFILES) -fPIC
"""

MAC_SONAME_PATCH = """
--- Makefile-libbz2_so
+++ Makefile-libbz2_so
@@ -37,3 +37,3 @@
 all: $(OBJS)
-\t$(CC) -shared -Wl,-soname -Wl,libbz2.so.1.0 -o libbz2.so.1.0.6 $(OBJS)
+\t$(CC) -shared -o libbz2.so.1.0.6 $(OBJS)
 \t$(CC) $(CFLAGS) -o bzip2-shared bzip2.c libbz2.so.1.0.6
"""


class Bzip2Conan(ConanFile):
    name = "Bzip2"
    version = "1.0.6-40"
    source_version = "1.0.6"
    license = "BSD-style"
    url = "http://www.bzip.org/"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=False"
    folder_name = "bzip2-%s" % source_version

    def source(self):
        zip_name = "%s.tar.gz" % self.folder_name
        url = "http://www.bzip.org/%s/%s" % (self.source_version, zip_name)
        self.output.info("Downloading %s" % url)
        tools.download(url, zip_name)
        tools.unzip(zip_name, ".")
        os.unlink(zip_name)

    def build(self):
        if self.options.shared and not self.options.fPIC:
            raise Exception(
                "shared library build requires fPIC option")

        if self.options.fPIC:
            self.output.info("Applying fPIC patch")
            tools.patch(patch_string=FPIC_PATCH, base_path=self.folder_name)

        if self.settings.os == "Macos" and self.options.shared:
            self.output.info("Applying Macos soname patch")
            tools.patch(patch_string=MAC_SONAME_PATCH,
                        base_path=self.folder_name)

        prefix = os.path.abspath("install")

        env_build = AutoToolsBuildEnvironment(self)
        env_vars = dict(env_build.vars)
        cflags = [env_vars["CFLAGS"]]
        ldflags = [env_vars["LDFLAGS"]]
        env_build.flags.append(cflags)
        with tools.environment_append(env_vars):
            self.output.info("Build environment: %s" % env_vars)
            self.run("cd %s && make -j%s install PREFIX=%s" %
                     (self.folder_name, tools.cpu_count(), prefix))
            if self.options.shared:
                self.run("cd %s && make -f Makefile-libbz2_so -j%s all" %
                         (self.folder_name, tools.cpu_count()))

    def package(self):
        self.copy("*.h", src="install/include", dst="include")
        if self.options.shared:
            self.copy("*.so.*", src=self.folder_name,
                      dst="lib", keep_path=False)
        else:
            self.copy("*.lib", src="install/lib", dst="lib", keep_path=False)
            self.copy("*.a", src="install/lib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["bz2"]
