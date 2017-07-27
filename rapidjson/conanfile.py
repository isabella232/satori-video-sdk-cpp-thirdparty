from conans import ConanFile


class RapidjsonConan(ConanFile):
    name = "Rapidjson"
    version = "1.1.0"
    license = "MIT"
    url = "https://github.com/miloyip/rapidjson.git"

    def source(self):
        self.run(
            "git clone -b v%s https://github.com/miloyip/rapidjson.git" % self.version)

    def package(self):
        self.copy("*", dst="include", src="rapidjson/include")
