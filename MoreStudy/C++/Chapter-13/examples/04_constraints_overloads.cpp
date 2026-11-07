#include <concepts>
#include <print>
#include <string_view>

template <std::integral T>
void show_type(T) { std::println("Integer input"); }

template <std::floating_point T>
void show_type(T) { std::println("Floating-point input"); }

void show_type(std::string_view) { std::println("Text input"); }

int main() {
    show_type(7);
    show_type(2.5);
    show_type(std::string_view{"ready"});
}
