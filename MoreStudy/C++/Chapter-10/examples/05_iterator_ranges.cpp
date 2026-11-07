#include <algorithm>
#include <iterator>
#include <print>
#include <vector>

int main() {
    const std::vector<int> samples{11, 13, 17, 19};
    const auto it = std::ranges::find(samples, 17);
    if (it != samples.end()) {
        const auto position = std::distance(samples.cbegin(), it);
        std::println("Found at index: {}", position);
    }
    std::println("Length: {}", std::ranges::distance(samples));
}
