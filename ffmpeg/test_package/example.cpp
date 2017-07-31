#include <assert.h>
#include <iostream>

extern "C" {
#include <libavcodec/avcodec.h>
}

int main() {
  avcodec_register_all();
  assert(avcodec_find_decoder_by_name("h264"));
  assert(avcodec_find_decoder_by_name("mjpeg"));
  assert(avcodec_find_decoder_by_name("rawvideo"));
  assert(avcodec_find_decoder_by_name("libvpx-vp9"));

  assert(avcodec_find_encoder_by_name("mjpeg"));
  assert(avcodec_find_encoder_by_name("jpeg2000"));
  assert(avcodec_find_encoder_by_name("libvpx-vp9"));
}
