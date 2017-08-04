from conans import ConanFile, CMake
import os


class OpencvConan(ConanFile):
    name = "Opencv"
    version = "3.3.0_01"
    source_version = "3.3.0"
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

        # enable OpenMP on linux
#        if self.settings.os != "Macos":
#            cmake_options.append("-DWITH_OPENMP=ON")

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
        self.cpp_info.libs =   ["opencv_stitching",
                                "opencv_optflow",
                                "opencv_aruco",
                                "opencv_ximgproc",
                                "opencv_xfeatures2d",
                                "opencv_videostab",
                                "opencv_tracking",
                                "opencv_structured_light",
                                "opencv_stereo",
                                "opencv_rgbd",
                                "opencv_datasets",
                                "opencv_ccalib",
                                "opencv_calib3d",
                                "opencv_text",
                                "opencv_saliency",
                                "opencv_line_descriptor",
                                "opencv_features2d",
                                "opencv_dpm",
                                "opencv_bioinspired",
                                "opencv_superres",
                                "opencv_highgui",
                                "opencv_xobjdetect",
                                "opencv_videoio",
                                "opencv_shape",
                                "opencv_imgcodecs",
                                "opencv_fuzzy",
                                "opencv_face",
                                "opencv_dnn",
                                "opencv_bgsegm",
                                "opencv_xphoto",
                                "opencv_video",
                                "opencv_surface_matching",
                                "opencv_reg",
                                "opencv_plot",
                                "opencv_photo",
                                "opencv_phase_unwrapping",
                                "opencv_objdetect",
                                "opencv_ml",
                                "opencv_imgproc",
                                "opencv_flann",
                                "opencv_core",
                                "libprotobuf",
                                "libpng",
                                "libjpeg",
                                "z",
                                "pthread"]

        if self.settings.os == "Macos":
            self.cpp_info.exelinkflags.append("-framework Foundation")
            self.cpp_info.exelinkflags.append("-framework AppKit")
