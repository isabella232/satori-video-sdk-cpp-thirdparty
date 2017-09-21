from conans import ConanFile


class BeastConan(ConanFile):
    name = "Beast"
    version = "117"
    tag = "0f5ea371c18a6797f4623a61f159326428c01400"
    license = "MIT"
    url = "https://github.com/boostorg/beast"
    requires = "Boost/1.64.0@satorivideo/master"

    def source(self):
        self.run("git clone https://github.com/boostorg/beast")
        self.run("cd beast && git checkout %s" % self.tag)

    def package(self):
        self.copy("*", dst="include", src="beast/include")
