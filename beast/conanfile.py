from conans import ConanFile


class BeastConan(ConanFile):
    name = "Beast"
    
    version = "123"
    tag = "885b9dfe0b6bfc7be6a9158d60f0760aa43e748a"
    git_url = "https://github.com/boostorg/beast.git"

    license = "MIT"
    url = "https://github.com/boostorg/beast"
    requires = "Boost/1.65.1-05@satorivideo/master"

    def source(self):
        self.run("git clone %s " % self.git_url)
        self.run("cd beast && git checkout %s" % self.tag)

    def package(self):
        self.copy("*", dst="include", src="beast/include")
