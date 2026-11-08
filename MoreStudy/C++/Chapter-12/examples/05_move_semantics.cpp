#include <iostream>
#include <string>
#include <utility>

int main() {
    std::string source{"sensor-packet"};
    std::string target = std::move(source);
    std::cout << "Target: " << target << '\n';
    // 이동 이후의 source 내용은 가정하지 않고 새 값을 대입합니다.
    source = "reused";
    std::cout << "Source: " << source << '\n';
}
