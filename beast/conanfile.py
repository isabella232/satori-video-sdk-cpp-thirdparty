from conans import ConanFile


class BeastConan(ConanFile):
    name = "Beast"
    version = "95"
    tag = "e3c79edebd94c1ac029466e4b172a6a9f04ba252"
    license = "MIT"
    url = "https://github.com/boostorg/beast"
    requires = "Boost/1.64.0@satorivideo/master"

    def source(self):
        self.run("git clone https://github.com/boostorg/beast")
        self.run("cd beast && git checkout %s" % self.tag)

    def package(self):
        self.copy("*", dst="include", src="beast/include")
