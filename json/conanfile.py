from conans import ConanFile, tools


class JsonConan(ConanFile):
    name = "Json"
    version = "2.1.1"
    license = "MIT"
    url = "https://github.com/nlohmann/json"
    # No settings/options are necessary, this is header only

    def source(self):
        # Entire repository is ~300MB, so it's better to download only header file
        url = "https://github.com/nlohmann/json/releases/download/v%s/json.hpp" % self.version
        self.output.info("Downloading %s" % url)
        tools.download(url, "json.hpp")

    def package(self):
        self.copy("*.hpp", "include")