#include <print>
#include <ranges>

int main() {
    for (const int sample_number : std::views::iota(1, 6)) {
        std::println("Processing sample {}", sample_number);
    }
}
