#include <iostream>
#include <string>
#include <string_view>

[[nodiscard]] std::size_t length(std::string_view text) { return text.size(); }
int main() {
    std::string owned{"sensor-name"};
    std::string copied = owned;
    std::string_view borrowed = owned;
    std::cout << "Copy size: " << copied.size()
              << ", View size: " << length(borrowed) << "\n";
    // borrowed는 owned보다 오래 사용하지 않음.
}
