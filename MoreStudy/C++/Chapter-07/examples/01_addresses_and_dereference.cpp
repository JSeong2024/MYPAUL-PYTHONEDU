#include <print>

int main() {
    int temperature{24};
    int* reading{&temperature};

    std::println("Original: {} C", temperature);
    *reading = 26;
    std::println("Updated: {} C", temperature);
    std::println("Same object: {}", reading == &temperature);
}
