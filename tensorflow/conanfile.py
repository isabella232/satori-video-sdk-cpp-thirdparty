from conans import ConanFile, tools
import os
import sys


class TensorflowConan(ConanFile):
    name = "Tensorflow"
    version = "1.4.0-rc0"
    revision = "v1.4.0-rc0"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    settings = "os", "compiler", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

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

        bazel_opts = ["-c opt",
                      # https://github.com/tensorflow/tensorflow/issues/7449
                      "--copt=-mavx",
                      "--copt=-msse4.2",
                      "--copt=-msse4.1",
                      "--copt=-msse3",
                      "--copt=-mavx2",
                      "--copt=-mfma"]

        if self.settings.os == "Linux":
            env["TF_NEED_MKL"] = "1"
            env["TF_DOWNLOAD_MKL"] = "1"
            bazel_opts.append("--config=mkl")

        if self.settings.compiler == "gcc":
            if self.settings.compiler.libcxx == "libstdc++":
                bazel_opts.append("--cxxopt=\"-D_GLIBCXX_USE_CXX11_ABI=0\"")
            else:
                bazel_opts.append("--cxxopt=\"-D_GLIBCXX_USE_CXX11_ABI=1\"")

        with tools.environment_append(env):
            self.output.info("Configuring build environment: %s" % env)
            self.run("cd tensorflow && ./configure")
            self.output.info("Using bazel options: %s" % " ".join(bazel_opts))
            self.run(
                "cd tensorflow/ && bazel build %s //tensorflow:libtensorflow_cc.so" % " ".join(bazel_opts))

            if self.settings.os == "Macos" or self.settings.os == "Linux":
                self.run("cd tensorflow/bazel-bin/tensorflow/ && chmod +x *.so")

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

        if self.settings.os == "Linux":
            self.copy("*.so", dst="lib",
                      src="./tensorflow/bazel-tensorflow/external/mkl/lib/", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["tensorflow_cc", "tensorflow_framework", "z"]

        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["libmklml_intel.so", "libiomp5.so"])

        lib_dir = os.path.join(self.package_folder, "lib")
        if self.settings.os == "Macos":
            self.env_info.DYLD_LIBRARY_PATH.append(lib_dir)
        if self.settings.os == "Linux":
            self.env_info.LD_LIBRARY_PATH.append(lib_dir)
