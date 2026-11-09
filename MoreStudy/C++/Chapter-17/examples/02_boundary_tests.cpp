#include <array>
#include <iostream>
#include <stdexcept>
bool valid_percent(int value) noexcept { return value >= 0 && value <= 100; }
int main() {
    struct Case { int input; bool expected; };
    const std::array cases{Case{-1,false}, Case{0,true}, Case{1,true},
                           Case{99,true}, Case{100,true}, Case{101,false}};
    for (const auto& c: cases) {
        if (valid_percent(c.input) != c.expected) throw std::runtime_error("boundary");
    }
    std::cout << "PASS: 6 boundaries\n";
}
