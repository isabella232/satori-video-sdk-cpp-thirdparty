#include <boost/filesystem.hpp>
#include <iostream>

int main() {
  boost::filesystem::path p = boost::filesystem::unique_path("%%%%");
  std::cout << "unique_path=" << p << "\n";
  std::cout << "boost::filesystem library is good.\n";
}
