from conans import ConanFile


class BeastConan(ConanFile):
    name = "Beast"
    
    version = "122_experimental"
    tag = "f09b2d3e1c9d383e5d0f57b1bf889568cf27c39f"
    git_url = "https://github.com/vinniefalco/beast.git"

    license = "MIT"
    url = "https://github.com/boostorg/beast"
    requires = "Boost/1.64.0@satorivideo/master"

    def source(self):
        self.run("git clone %s " % self.git_url)
        self.run("cd beast && git checkout %s" % self.tag)

    def package(self):
        self.copy("*", dst="include", src="beast/include")
