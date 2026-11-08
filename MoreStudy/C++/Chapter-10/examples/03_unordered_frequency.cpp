#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

int main() {
    const std::vector<std::string> events{"WARN", "INFO", "WARN", "ERROR", "INFO"};
    std::unordered_map<std::string, int> counts;
    counts.reserve(3);
    for (const auto& event : events) {
        ++counts[event];
    }

    // 해시 테이블의 순회 순서는 보장되지 않으므로 키를 지정해 출력합니다.
    std::cout << "INFO: " << counts.at("INFO") << '\n';
    std::cout << "WARN: " << counts.at("WARN") << '\n';
    std::cout << "ERROR: " << counts.at("ERROR") << '\n';
    std::cout << std::boolalpha << "Contains DEBUG: " << counts.contains("DEBUG") << '\n';
}
