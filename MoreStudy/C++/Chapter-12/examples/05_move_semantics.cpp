#include <print>
#include <string>
#include <utility>

int main() {
    std::string source{"sensor-packet"};
    std::string target = std::move(source);
    std::println("Target: {}", target);
    // 이동 후 source는 유효하지만 내용은 특정하지 않음
    source = "reused";
    std::println("Source: {}", source);
}
