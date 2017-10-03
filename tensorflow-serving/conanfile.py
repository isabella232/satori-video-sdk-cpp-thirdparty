from conans import ConanFile, tools
import os
import sys


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

        lib_dirs = [
            "./serving/bazel-bin/external/org_tensorflow/tensorflow/core/",
            "./serving/bazel-bin/external/protobuf_archive",
            "./serving/bazel-bin/external/nsync",
            "./serving/bazel-bin/external/png_archive",
            "./serving/bazel-bin/external/snappy",
        ]
        for d in lib_dirs:
            self.copy("*.lo", dst="lib", src=d,
                      keep_path=True, excludes="*.runfiles*")
            self.copy("*.so", dst="lib", src=d,
                      keep_path=True, excludes="*.runfiles*")
            self.copy("*.a", dst="lib", src=d,
                      keep_path=True, excludes="*.runfiles*")

    def package_info(self):
        self.cpp_info.libs = ["framework_internal",
                              "lib_internal", "lib_proto_parsing", "core_cpu_internal",
                              "lib_hash_crc32c_accelerate_internal", "version_lib",
                              "proto_text", "protos_all_cc", "protobuf", "protobuf_lite",
                              "nsync_cpp", "png", "snappy", "z"]

        self.env_info.DYLD_LIBRARY_PATH.append(
            os.path.join(self.package_folder, "lib"))

        self.env_info.LD_LIBRARY_PATH.append(
            os.path.join(self.package_folder, "lib"))

        self.env_info.FOOOOOOOOOOOOOOOOOOOOO.append(
            os.path.join(self.package_folder, "lib"))

        # self.cpp_info.libdirs = [
        #     "lib/external/org_tensorflow/tensorflow/core/",
        #     "lib/external/protobuf_archive",
        # ]

        # print "***", self.env_info.DYLD_LIBRARY_PATH
