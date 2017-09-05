from conans import ConanFile, tools
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

class Bzip2Conan(ConanFile):
    name = "Bzip2"
    version = "1.0.6"
    license = "BSD-style"
    url = "http://www.bzip.org/"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=False"
    folder_name = "bzip2-%s" % version

    def source(self):
        zip_name = "%s.tar.gz" % self.folder_name
        url = "http://www.bzip.org/%s/%s" % (self.version, zip_name)
        self.output.info("Downloading %s" % url)
        tools.download(url, zip_name)
        tools.unzip(zip_name, ".")
        os.unlink(zip_name)

    def build(self):
        if self.options.shared:
            raise Exception("shared library build currently is not supported for bzip2")

        if self.options.fPIC:
            self.output.info("Applying fPIC patch")
            tools.patch(patch_string=FPIC_PATCH, base_path=self.folder_name)

        prefix = os.path.abspath("install")
        self.run("cd %s && make -j%s install PREFIX=%s" % (self.folder_name, tools.cpu_count(), prefix))

    def package(self):
        self.copy("*.h", src="install/include", dst="include")
        if self.options.shared:
            self.copy("*.dll", src="install/lib", dst="bin", keep_path=False)
            self.copy("*.so", src="install/lib", dst="lib", keep_path=False)
            self.copy("*.so.*", src="install/lib", dst="lib", keep_path=False)
            self.copy("*.dylib", src="install/lib", dst="lib", keep_path=False)
        else:
            self.copy("*.lib", src="install/lib", dst="lib", keep_path=False)
            self.copy("*.a", src="install/lib", dst="lib", keep_path=False)


    def package_info(self):
        self.cpp_info.libs = ["bz2"]
