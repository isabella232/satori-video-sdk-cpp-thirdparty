#include <stdio.h>
extern "C" {
#include <darknet.h>
}

int main(int argc, char *argv[]) {
  image i = make_image(320, 200, 3);
  free_image(i);
}
