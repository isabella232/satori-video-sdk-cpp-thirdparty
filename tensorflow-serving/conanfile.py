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

    tf_libraries = [
        "serving/bazel-bin/external/jpeg/jpeg",
        "serving/bazel-bin/external/jpeg/simd_none",
        "serving/bazel-bin/external/nsync/nsync_cpp",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/cc/cc_ops_internal",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/cc/cc_ops",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/core_cpu_internal",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/framework_internal",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/gif_internal",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/jpeg_internal",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/lib_hash_crc32c_accelerate_internal",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/lib_internal",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/lib_proto_parsing",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/proto_text",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/protos_all_cc",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/reader_base",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/sycl_runtime",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/version_lib",
        "serving/bazel-bin/external/png_archive/png",
        "serving/bazel-bin/external/protobuf_archive/protobuf_lite",
        "serving/bazel-bin/external/protobuf_archive/protobuf",
        "serving/bazel-bin/external/snappy/snappy"
    ]

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
            self.run("cd serving && ls -R")

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

        for lib in self.tf_libraries:
            d = os.path.dirname(lib)
            f = os.path.basename(lib)

            self.output.info("copying  lib%s from %s" % (f, d))
            self.copy("lib%s.lo" % f, dst="lib",
                      src=d, keep_path=False)
            self.copy("lib%s.so" % f, dst="lib",
                      src=d, keep_path=False)
            self.copy("lib%s.a" % f, dst="lib",
                      src=d, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [os.path.basename(
            lib) for lib in self.tf_libraries]
        self.cpp_info.libs.append("z")

        # lib_dir = os.path.join(self.package_folder, "lib")

        # self.env_info.DYLD_LIBRARY_PATH.append(lib_dir)
        # self.env_info.LD_LIBRARY_PATH.append(lib_dir)
        # self.env_info.FOOOOOOOOOOOOOOOOOOOOO.append(lib_dir)

        # self.cpp_info.libdirs = [
        #     "./lib",
        #     "./lib/bazel-bin/external/org_tensorflow/tensorflow/core/",
        #     "./lib/bazel-bin/external/protobuf_archive",
        #     "./lib/bazel-bin/external/nsync",
        #     "./lib/bazel-bin/external/png_archive",
        #     "./lib/bazel-bin/external/snappy",
        #     #     "lib/external/org_tensorflow/tensorflow/core/",
        #     #     "lib/external/protobuf_archive",
        # ]

        # print "***", self.env_info.DYLD_LIBRARY_PATH
