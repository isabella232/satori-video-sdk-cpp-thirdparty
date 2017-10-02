from conans import ConanFile, tools
import sys
import traceback


class TensorflowservingConan(ConanFile):
    name = "TensorflowServing"
    version = "1.3.0_master"
    tag = "6330edb4bb7002b3bf8d32860c2e7fb0d5ab0a16"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run(
            "git clone --recurse-submodules --depth 1 https://github.com/tensorflow/serving")
        self.run("cd serving && git checkout %s" % self.tag)

    def build(self):
        env = {
            "PYTHON_BIN_PATH": sys.executable,
            "USE_DEFAULT_PYTHON_LIB_PATH": "1",
            "CC_OPT_FLAGS": "-march=native",
            "TF_NEED_MKL": "0",
            "TF_NEED_GCP": "0",
            "TF_NEED_HDFS": "0",
            "TF_ENABLE_XLA": "0",
            "TF_NEED_VERBS": "0",
            "TF_NEED_OPENCL": "0",
            "TF_NEED_CUDA": "0",
            "TF_NEED_MPI": "0",
            "TF_NEED_GDR": "0",
            "TF_NEED_JEMALLOC": "0",
        }
        with tools.environment_append(env):
            self.output.info("Build environment: %s" % env)
            self.run("cd serving/tensorflow && ./configure")
            self.run("cd serving/ && bazel build -c opt tensorflow_serving/...")

    def package(self):
        # header files
        self.copy("*.h", dst="include", src="./serving/tensorflow/")
        self.copy("*.h", dst="include",
                  src="./serving/tf_models/syntaxnet/tensorflow/")
        self.copy("*", dst="include",
                  src="./serving/bazel-serving/external/eigen_archive/")
        self.copy("*", dst="include/third_party/eigen3",
                  src="./serving/tensorflow/third_party/eigen3/")
        self.copy("*.h", dst="include",
                  src="./serving/bazel-genfiles/external/org_tensorflow/")
        self.copy("*.h", dst="include",
                  src="./serving/bazel-serving/external/protobuf_archive/src/")
        self.copy("*.h", dst="include",
                  src="./serving/bazel-serving/external/nsync/public/")

        # libraries
        self.copy("*.so", dst="lib",
                  src="./serving/bazel-bin/", keep_path=True,
                  excludes="*.runfiles*")
        self.copy("*.so", dst="lib",
                  src="./serving/bazel-out/", keep_path=True,
                  excludes="*.runfiles*")

    def package_info(self):
        self.cpp_info.libs = ["framework_internal",
                              "lib_internal", "core_cpu_internal", "protos_all_cc"]
        self.cpp_info.libdirs = [
            "lib/external/org_tensorflow/tensorflow/core/"]
