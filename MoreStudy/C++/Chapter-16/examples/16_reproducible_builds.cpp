#include <iostream>
#include <string_view>
[[nodiscard]] bool valid_identifier(std::string_view id) {
    if (id.empty()) return false;
    for (unsigned char ch : id) {
        if (!((ch >= 'A' && ch <= 'Z') || (ch >= '0' && ch <= '9') || ch == '-')) return false;
    }
    return true;
}
int main() {
    std::cout << "Valid: " << std::boolalpha << valid_identifier("SENSOR-12") << '\n';
}
