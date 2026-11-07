#include <print>
#include <string>
#include <string_view>

[[nodiscard]] std::string_view first_word(std::string_view input) {
    const auto pos = input.find(' ');
    return input.substr(0, pos);
}

int main() {
    const std::string message{"sensor ready"};
    const std::string_view borrowed = first_word(message);
    std::println("Borrowed: {}", borrowed);
    const std::string owned{borrowed}; // 별도 수명이 필요하면 복사하여 소유
    std::println("Owned: {}", owned);
}
