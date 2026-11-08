#include <iostream>
#include <map>
#include <string>

int main() {
    int count = 0;
    if (!(std::cin >> count) || count < 0 || count > 100000) {
        std::cout << "INVALID\n";
        return 0;
    }
    std::map<std::string, int> frequency;
    for (int i = 0; i < count; ++i) {
        std::string code;
        if (!(std::cin >> code)) {
            std::cout << "INVALID\n";
            return 0;
        }
        ++frequency[code];
    }
    for (const auto& [code, times] : frequency) {
        std::cout << code << ' ' << times << '\n';
    }
}
