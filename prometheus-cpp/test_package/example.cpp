#include <prometheus/counter.h>
#include <iostream>

int main() {
  prometheus::Counter counter;
  counter.Increment();
}
