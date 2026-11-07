#include <print>
#include <string>
#include <string_view>

[[nodiscard]] std::string_view category_of(std::string_view identifier) {
    const auto delimiter = identifier.find(':');
    if (delimiter == std::string_view::npos) {
        return {};
    }
    return identifier.substr(0, delimiter);
}

int main() {
    const std::string identifier{"MOTOR:FRONT-LEFT"};
    const std::string_view category = category_of(identifier);
    std::println("Category: {}", category);
    // category는 identifier가 살아 있는 동안에만 유효함.
}
