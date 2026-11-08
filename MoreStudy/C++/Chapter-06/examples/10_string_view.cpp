#include <iostream>
#include <string>
#include <string_view>

[[nodiscard]] std::string_view category_of(std::string_view identifier) {
    const auto separator = identifier.find(':');
    if (separator == std::string_view::npos) return {};
    return identifier.substr(0, separator);
}

int main() {
    const std::string owned{"MOTOR:FRONT-LEFT"};
    const std::string_view category = category_of(owned);
    std::cout << "Category: " << category << '\n';
}
