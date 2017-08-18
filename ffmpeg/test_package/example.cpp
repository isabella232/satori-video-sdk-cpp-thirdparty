#include <iostream>
#include <string>
#include <vector>

extern "C" {
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
}

int main() {
  std::cout << "*** Running ffmpeg library check\n";

  avcodec_register_all();
  av_register_all();

  std::vector<std::string> decoders;
  decoders.push_back("h264");
  decoders.push_back("mjpeg");
  decoders.push_back("rawvideo");
  decoders.push_back("libvpx-vp9");
  for (const std::string &d : decoders) {
    if (!avcodec_find_decoder_by_name(d.c_str())) {
      std::cout << "*** Didn't find decoder " << d << "\n";
      return 1;
    }
  }

  std::vector<std::string> encoders;
  encoders.push_back("mjpeg");
  encoders.push_back("jpeg2000");
  encoders.push_back("libvpx-vp9");
  for (const std::string &e : encoders) {
    if (!avcodec_find_encoder_by_name(e.c_str())) {
      std::cout << "*** Didn't find encoder " << e << "\n";
      return 1;
    }
  }

  std::vector<std::string> output_formats;
  output_formats.push_back("matroska");
  for (const std::string &of : output_formats) {
    if (!av_guess_format(of.c_str(), nullptr, nullptr)) {
      std::cout << "*** Didn't find output format " << of << "\n";
      return 1;
    }
  }

  std::cout << "*** FFmpeg library check succeeded\n";
  return 0;
}
