#include "device/validator.hpp"
namespace device {
bool is_valid(int value) noexcept { return value>=0 && value<=100; }
std::size_t count_valid(std::span<const int> values) noexcept {
 std::size_t count=0;
 for(int value:values) if(is_valid(value)) ++count;
 return count;
}
}
