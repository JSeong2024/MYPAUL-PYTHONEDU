#include <iostream>
#include <string>
#include <string_view>

void print_device(const std::string& name) {
    std::cout << "Device: " << name << '\n';
}

bool has_prefix(std::string_view name) {
    return name.starts_with("DEV-");
}

int main() {
    const std::string name{"DEV-42"};
    print_device(name);
    std::cout << std::boolalpha << "Valid prefix: " << has_prefix(name) << '\n';
}
