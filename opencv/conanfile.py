from conans import ConanFile, CMake
import os


class OpencvConan(ConanFile):
    name = "Opencv"
    version = "3.2.0_01"
    source_version = "3.2.0"
    license = "3-clause BSD License"
    url = "http://opencv.org/"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "fPIC": [True, False],
               "with_ipp": [True, False]}
    default_options = "shared=False", "fPIC=False", "with_ipp=False"
    generators = "cmake"

    def source(self):
        self.run(
            "git clone --depth 1 -b %s https://github.com/opencv/opencv.git" % self.source_version)
        self.run(
            "git clone --depth 1 -b %s https://github.com/opencv/opencv_contrib.git" % self.source_version)

    def build(self):
        cmake = CMake(self)

        cmake_options = []
        cmake_options.append("-GNinja")
        cmake_options.append("-DCMAKE_VERBOSE_MAKEFILE=ON")

        # turn off extra deps
        cmake_options.append("-DWITH_GSTREAMER=OFF")
        cmake_options.append("-DWITH_JASPER=OFF")
        cmake_options.append("-DWITH_ITT=OFF")
        cmake_options.append("-DWITH_LAPACK=OFF")
        cmake_options.append("-DWITH_OPENCL=OFF")
        cmake_options.append("-DWITH_OPENEXR=OFF")
        cmake_options.append("-DWITH_TIFF=OFF")
        cmake_options.append("-DWITH_WEBP=OFF")

        # turn off extra targets
        cmake_options.append("-DBUILD_EXAMPLES=OFF")
        cmake_options.append("-DBUILD_opencv_apps=OFF")
        cmake_options.append("-DBUILD_TESTS=OFF")
        cmake_options.append("-DBUILD_PERF_TESTS=OFF")
        cmake_options.append("-DENABLE_CCACHE=OFF")

        # build options
        cmake_options.append("-DCMAKE_BUILD_TYPE=%s" %
                             self.settings.build_type)
        cmake_options.append("-DCMAKE_INSTALL_PREFIX=install")
        cmake_options.append("-DBUILD_SHARED_LIBS=%s" %
                             ("ON" if self.options.shared else "OFF"))
        cmake_options.append("-DOPENCV_EXTRA_MODULES_PATH=opencv_contrib/modules")
        if self.options.fPIC:
            cmake_options.append("-DCMAKE_C_FLAGS=-fPIC")
            cmake_options.append("-DCMAKE_CXX_FLAGS=-fPIC")
        cmake_options.append("-DWITH_IPP=%s" %
                             ("ON" if self.options.with_ipp else "OFF"))

        self.output.info("Using cmake options: %s" % " ".join(cmake_options))

        self.run('cmake opencv %s %s' %
                 (cmake.command_line, " ".join(cmake_options)))
        self.run("cmake --build . %s --target install" % cmake.build_config)

    def package(self):
        self.copy("*", src="3rdparty/lib", dst="lib", keep_path=False)
        self.copy("*", src="install")

    def package_info(self):
        # imgcodecs: imgproc
        self.cpp_info.libs =   ["opencv_aruco",
                                "opencv_stereo",
                                "opencv_tracking",
                                "opencv_bgsegm",
                                "opencv_stitching",
                                "opencv_bioinspired",
                                "opencv_structured_light",
                                "opencv_videoio",
                                "opencv_video",
                                "opencv_calib3d",
                                "opencv_line_descriptor",
                                "opencv_superres",
                                "opencv_ccalib",
                                "opencv_ml",
                                "opencv_surface_matching",
                                "opencv_objdetect",
                                "opencv_imgcodecs",
                                "opencv_imgproc",
                                "opencv_text",
                                "opencv_datasets",
                                "opencv_optflow",
                                "opencv_dnn",
                                "opencv_phase_unwrapping",
                                "opencv_dpm",
                                "opencv_photo",
                                "opencv_face",
                                "opencv_plot",
                                "opencv_videostab",
                                "opencv_features2d",
                                "opencv_reg",
                                "opencv_xfeatures2d",
                                "opencv_flann",
                                "opencv_rgbd",
                                "opencv_ximgproc",
                                "opencv_fuzzy",
                                "opencv_saliency",
                                "opencv_xobjdetect",
                                "opencv_highgui",
                                "opencv_shape",
                                "opencv_xphoto",
                                "opencv_core",
                                "libjpeg",
                                "libpng",
                                "libprotobuf",
                                "z",
                                "pthread"]

        if self.settings.os == "Macos":
            self.cpp_info.exelinkflags.append("-framework Foundation")
            self.cpp_info.exelinkflags.append("-framework AppKit")
