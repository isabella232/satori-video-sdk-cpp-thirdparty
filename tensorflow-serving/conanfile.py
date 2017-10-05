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
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/core_cpu_base",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/core_cpu_internal",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/framework_internal",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/gif_internal",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/jpeg_internal",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/lib_internal",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/lib_hash_crc32c_accelerate_internal",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/lib_proto_parsing",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/proto_text",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/shape_inference_testutil",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/protos_all_cc",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/reader_base",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/sycl_runtime",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/version_lib",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/tensor_testutil",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/test",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/kernels/captured_function",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/kernels/conditional_accumulator_base",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/kernels/dataset",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/kernels/fifo_queue",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/kernels/fill_functor",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/kernels/fused_batch_norm_util_gpu",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/kernels/initializable_lookup_table",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/kernels/linalg_ops_common",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/kernels/lookup_util",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/kernels/mfcc",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/kernels/mfcc_dct",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/kernels/mfcc_mel_filterbank",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/kernels/ops_util",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/kernels/padding_fifo_queue",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/kernels/priority_queue",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/kernels/queue_base",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/kernels/range_sampler",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/kernels/remote_fused_graph_execute_utils",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/kernels/save_restore_tensor",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/kernels/sdca_internal",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/kernels/spectrogram",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/kernels/training_op_helpers",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/kernels/warn_about_ints",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/core/kernels/window_dataset",
        "serving/bazel-bin/external/org_tensorflow/tensorflow/stream_executor/stream_executor",
        "serving/bazel-bin/external/png_archive/png",
        "serving/bazel-bin/external/protobuf_archive/protobuf_lite",
        "serving/bazel-bin/external/protobuf_archive/protobuf",
        "serving/bazel-bin/external/nsync/nsync_cpp",
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
        for lib in self.tf_libraries:
            d = os.path.dirname(lib)
            self.output.info("dir %s:" % d)
            self.run("cd %s && ls -R" % d)

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

        lib_dir = os.path.join(self.package_folder, "lib")
        if self.settings.os == "Macos":
            self.env_info.DYLD_LIBRARY_PATH.append(lib_dir)
        if self.settings.os == "Linux":
            self.env_info.LD_LIBRARY_PATH.append(lib_dir)
