#include "echo.hpp"
#include <stdexcept>
#include <string>
void check(bool condition) { if (!condition) throw std::runtime_error("assertion failed"); }
int main() {
    check(echo::round_trip("hello") == "hello");
    check(echo::round_trip("").empty());
    const std::string binary{"\0X",2};
    check(echo::round_trip(binary) == binary);
    try { (void)echo::round_trip(std::string(4097, 'x')); }
    catch (const std::length_error&) { return 0; }
    return 1;
}
