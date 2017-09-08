from conans import ConanFile


class LoguruConan(ConanFile):
    name = "Loguru"
    version = "1.5.1"
    tag = "75606d74bd1d374e8525a53db91f054b8b7d4cac"
    license = "custom"
    url = "https://github.com/emilk/loguru"
    # No settings/options are necessary, this is header only

    def source(self):
        self.run("git clone --depth 1 https://github.com/emilk/loguru")
        self.run("cd loguru && git checkout %s" % self.tag)

    def package(self):
        self.copy("*.hpp", "include")
        
    def package_info(self):
        self.cpp_info.libs = ["pthread", "dl"]
