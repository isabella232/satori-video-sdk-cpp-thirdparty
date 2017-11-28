#include <iostream>

#include "json.hpp"

using json = nlohmann::json;

int main() {
  json obj = {{"pi", 3.141},
              {"happy", true},
              {"name", "Niels"},
              {"nothing", nullptr},
              {"answer", {{"everything", 42}}},
              {"list", {1, 0, 2}},
              {"object", {{"currency", "USD"}, {"value", 42.99}}}};

  std::cout << "Test object is " << obj << "\n";

  std::cout << "Json library is good.\n";
}
