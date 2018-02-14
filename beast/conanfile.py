from conans import ConanFile


class BeastConan(ConanFile):
    name = "Beast"
    
    version = "1.66.0"
    tag = "boost-1.66.0"
    git_url = "https://github.com/boostorg/beast.git"

    license = "MIT"
    url = "https://github.com/boostorg/beast"
    requires = "Boost/1.66.0-03@satorivideo/master"

    def source(self):
        self.run("git clone %s " % self.git_url)
        self.run("cd beast && git checkout %s" % self.tag)

    def package(self):
        self.copy("*", dst="include", src="beast/include")
