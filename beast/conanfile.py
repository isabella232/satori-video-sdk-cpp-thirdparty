from conans import ConanFile


class BeastConan(ConanFile):
    name = "Beast"
    version = "89"
    tag = "c7b830f37f8adc0df63d41ff4d31395ab704516b"
    license = "MIT"
    url = "https://github.com/boostorg/beast"
    requires = "Boost/1.64.0@satorivideo/master"

    def source(self):
        self.run("git clone https://github.com/boostorg/beast")
        self.run("cd beast && git checkout %s" % self.tag)

    def package(self):
        self.copy("*", dst="include", src="beast/include")
