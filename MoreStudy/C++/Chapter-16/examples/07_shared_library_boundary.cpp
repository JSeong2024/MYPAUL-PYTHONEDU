#include <iostream>
#include <string_view>
[[nodiscard]] bool needs_attention(std::string_view device, int reading) {
    return !device.empty() && reading >= 80;
}
int main() {
    std::cout << "Alert: " << std::boolalpha << needs_attention("motor", 85) << '\n';
}
