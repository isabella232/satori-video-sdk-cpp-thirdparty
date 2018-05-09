#include <iostream>
#include <sstream>
#include <string>
#include <vector>

extern "C" {
#include <libavcodec/avcodec.h>
#include <libavfilter/avfilter.h>
#include <libavformat/avformat.h>
}

int main() {
  std::cout << "*** Running ffmpeg library check\n";

  avcodec_register_all();
  avfilter_register_all();
  av_register_all();

  AVCodec *codec = av_codec_next(nullptr);
  while (codec != nullptr) {
    std::cout << "*** Got codec: " << codec->name << "\n";
    codec = av_codec_next(codec);
  }

  std::vector<std::string> decoders{"h264", "mjpeg", "rawvideo",
                                    "libvpx" /* vp8 */, "libvpx-vp9" /* vp9 */};
  for (const std::string &d : decoders) {
    if (!avcodec_find_decoder_by_name(d.c_str())) {
      std::cerr << "*** Didn't find decoder '" << d << "'\n";
      return 1;
    }

    std::cout << "*** Found decoder '" << d << "'\n";
  }

  std::vector<std::string> encoders{"mjpeg", "jpeg2000", "libvpx-vp9", "srt"};
  for (const std::string &e : encoders) {
    if (!avcodec_find_encoder_by_name(e.c_str())) {
      std::cerr << "*** Didn't find encoder '" << e << "'\n";
      return 1;
    }

    std::cout << "*** Found encoder '" << e << "'\n";
  }

  std::vector<std::string> output_formats{"matroska", "mp4"};
  for (const std::string &of : output_formats) {
    if (!av_guess_format(of.c_str(), nullptr, nullptr)) {
      std::cerr << "*** Didn't find output format '" << of << "'\n";
      return 1;
    }

    std::cout << "*** Found output format '" << of << "'\n";
  }

  std::vector<std::string> bitstream_filters{"vp9_superframe"};
  for (const std::string &bsf : bitstream_filters) {
    if (!av_bsf_get_by_name(bsf.c_str())) {
      std::cerr << "*** Didn't find bitstream filter '" << bsf << "'\n";
      return 1;
    }

    std::cout << "*** Found bitstream filter '" << bsf << "'\n";
  }

  std::vector<std::string> input_formats{"mp4", "matroska", "webm"};
  for (const std::string &f : input_formats) {
    if (!av_find_input_format(f.c_str())) {
      std::cerr << "*** Didn't find input format '" << f << "'\n";
      return 1;
    }

    std::cout << "*** Found input format '" << f << "'\n";
  }

  const std::vector<std::string> expected_filters{"hflip", "vflip", "rotate",
                                                  "scale", "transpose"};
  for (const auto &f : expected_filters) {
    if (!avfilter_get_by_name(f.c_str())) {
      std::cerr << "*** Didn't find filter '" << f << "'\n";
      return 1;
    }
    std::cout << "*** Found filter '" << f << "'\n";
  }

  std::ostringstream filters_buffer;
  const AVFilter *filter{nullptr};
  while ((filter = avfilter_next(filter)) != nullptr) {
    if (filters_buffer.tellp() > 0) {
      filters_buffer << ", ";
    }
    filters_buffer << filter->name;
  }
  std::cout << "*** Got filters: " << filters_buffer.str() << "\n";

  std::cout << "*** FFmpeg library check succeeded\n";
  return 0;
}
