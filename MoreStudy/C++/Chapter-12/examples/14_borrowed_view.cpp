#include <iostream>
#include <span>
#include <string>
#include <string_view>
#include <vector>

void inspect(std::span<const int> values, std::string_view source) {
    std::cout << source << ": " << values.front() << '\n';
}

int main() {
    std::vector<int> readings{12, 14, 18};
    std::string name{"sensor-A"};
    inspect(readings, name);
    // readings/name이 살아 있는 동안에만 span/string_view가 유효합니다.
}
