#include "device/validator.hpp"
#include <array>
#include <iostream>
#include <stdexcept>
void expect(bool value) {if(!value)throw std::runtime_error("validator regression");}
int main() {
 expect(!device::is_valid(-1));expect(device::is_valid(0));
 expect(device::is_valid(100));expect(!device::is_valid(101));
 const std::array values{-1,0,49,100,101};
 expect(device::count_valid(values)==3);
 const std::array<int,0> empty{}; expect(device::count_valid(empty)==0);
 std::cout<<"Validator: PASS\n";
}
