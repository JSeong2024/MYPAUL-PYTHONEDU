#include "device/validator.hpp"
#include <array>
#include <iostream>
int main() {
 const std::array values{0,50,-1,101};
 std::cout << "Valid: " << device::count_valid(values) << '\n';
}
