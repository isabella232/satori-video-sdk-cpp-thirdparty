#include "bzlib.h"

int main() {
  bz_stream stream;
  stream.avail_in = 5;
  if (stream.avail_in != 5) {
    return 1;
  }
}
