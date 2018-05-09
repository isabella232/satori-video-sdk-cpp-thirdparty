from conans import ConanFile


class LoguruConan(ConanFile):
    name = "Loguru"
    version = "1.5.0-40"
    source_version = "1.5.0"
    license = "custom"
    url = "https://github.com/emilk/loguru"
    # No settings/options are necessary, this is header only

    def source(self):
        self.run("git clone -b v%s --depth 1 https://github.com/emilk/loguru" % self.source_version)

    def package(self):
        self.copy("*.hpp", "include")
        
    def package_info(self):
        self.cpp_info.libs = ["pthread", "dl"]
