from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class FfmpegConan(ConanFile):
    name = "Ffmpeg"
    version = "3.3.3"
    license = "LGPL"
    url = "https://ffmpeg.org/"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=False"
    requires = "Libvpx/1.6.1@satorivideo/master"

    def source(self):
        self.run(
            "git clone --depth 1 -b n%s https://github.com/FFmpeg/FFmpeg.git" % self.version)

    def build(self):
        configure_args = []

        prefix = os.path.abspath("install")
        configure_args.append("--prefix=%s" % prefix)
        if self.options.fPIC:
            configure_args.append("--enable-pic")
        if self.options.shared:
            configure_args.append("--enable-shared")
        if self.settings.build_type == "Debug":
            configure_args.append("--enable-debug=3")
            configure_args.append("--disable-stripping")

        # disable as much as possible
        configure_args.append("--disable-all")
        configure_args.append("--disable-programs")
        configure_args.append("--disable-everything")
        configure_args.append("--disable-sdl2")

        # enable libraries
        configure_args.append("--enable-avcodec")
        configure_args.append("--enable-avdevice")
        configure_args.append("--enable-avformat")
        configure_args.append("--enable-avutil")
        configure_args.append("--enable-swscale")
        configure_args.append("--enable-indev=avfoundation")

        # enable codecs/protocols
        configure_args.append("--enable-libvpx")
        configure_args.append("--enable-decoder=h264")
        configure_args.append("--enable-decoder=mjpeg")
        configure_args.append("--enable-decoder=libvpx_vp9")
        configure_args.append("--enable-encoder=libvpx_vp9")
        configure_args.append("--enable-decoder=rawvideo")
        configure_args.append("--enable-demuxer=mov")
        configure_args.append("--enable-encoder=jpeg2000")
        configure_args.append("--enable-encoder=mjpeg")
        configure_args.append("--enable-protocol=file")

        env_build = AutoToolsBuildEnvironment(self)
        env_vars = dict(env_build.vars)
        # env_vars["KERNEL_BITS"] = "64"
        with tools.environment_append(env_vars):
            self.output.info("Build environment: %s" % env_vars)
            self.output.info("configure %s" % " ".join(configure_args))
            self.run("cd ffmpeg && ./configure %s" %
                     " ".join(configure_args))
            self.run("cd ffmpeg && V=1 make -j%s all install" %
                     tools.cpu_count())

    def package(self):
        self.copy("*", src="install")

    def package_info(self):
        self.cpp_info.libs = ["avcodec", "avutil",
                              "avdevice", "avformat", "swscale"]

        if self.settings.os == "Macos":
            self.cpp_info.libs.append("iconv")