from conans import ConanFile, tools
import os
import sys


class TensorflowConan(ConanFile):
    name = "Tensorflow"
    version = "1.3.1_master"
    revision = "073d90578904aa00dee34e27d9cc6bac68af2c47"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

#    def configure(self):
#        if self.settings.os == "Macos":
#            self.tf_libraries.append(
#                "tensorflow/bazel-bin/external/jpeg/simd_none")

    def source(self):
        self.run(
            "git clone https://github.com/tensorflow/tensorflow && cd tensorflow && git checkout %s" % self.revision)

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

        bazel_opts = ["-c opt"]

        if self.settings.compiler == "gcc":
            if self.settings.compiler.libcxx == "libstdc++":
                bazel_opts.append("--cxxopt=\"-D_GLIBCXX_USE_CXX11_ABI=0\"")
            else:
                bazel_opts.append("--cxxopt=\"-D_GLIBCXX_USE_CXX11_ABI=1\"")

        with tools.environment_append(env):
            self.output.info("Build environment: %s" % env)
            self.output.info("Bazel options: %s" % " ".join(bazel_opts))
            self.run("cd tensorflow && ./configure")
            self.run(
                "cd tensorflow/ && bazel build %s //tensorflow:libtensorflow_cc.so" % " ".join(bazel_opts))

    def package(self):
        # header files
        self.copy("*.h", dst="include", src="./tensorflow/")
        self.copy("*", dst="include",
                  src="./tensorflow/bazel-tensorflow/external/eigen_archive/")
        self.copy("*", dst="include/third_party/eigen3",
                  src="./tensorflow/third_party/eigen3/")
        self.copy("*.h", dst="include",
                  src="./tensorflow/bazel-genfiles/external/org_tensorflow/")
        self.copy("*.h", dst="include/tensorflow/",
                  src="./tensorflow/bazel-genfiles/tensorflow/")
        self.copy("*.h", dst="include",
                  src="./tensorflow/bazel-tensorflow/external/protobuf_archive/src/")
        self.copy("*.h", dst="include",
                  src="./tensorflow/bazel-tensorflow/external/nsync/public/")
        self.copy("*.so", dst="lib",
                  src="./tensorflow/bazel-bin/tensorflow/", keep_path=False, excludes="*.runfiles/*")

    def package_info(self):
        self.cpp_info.libs = ["tensorflow_cc", "tensorflow_framework", "z"]

        lib_dir = os.path.join(self.package_folder, "lib")
        if self.settings.os == "Macos":
            self.env_info.DYLD_LIBRARY_PATH.append(lib_dir)
        if self.settings.os == "Linux":
            self.env_info.LD_LIBRARY_PATH.append(lib_dir)