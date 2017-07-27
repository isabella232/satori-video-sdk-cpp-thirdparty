from conans import ConanFile


class GslConan(ConanFile):
    name = "Gsl"
    version = "20017.07.27"
    tag = "2b8d20425e990c5a3e9a0158e2cedacbcdf9e522"
    license = "MIT"
    url = "https://github.com/Microsoft/GSL"

    def source(self):
        self.run("git clone https://github.com/Microsoft/GSL.git")
        self.run("cd GSL && git checkout %s" % self.tag)

    def package(self):
        self.copy("*", dst="include", src="GSL/include")
