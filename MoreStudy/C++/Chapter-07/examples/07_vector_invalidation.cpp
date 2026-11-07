#include <print>
#include <vector>

int main() {
    std::vector<int> samples{10, 20};
    const std::size_t index{1};

    // push_back 과정에서 재할당되면 기존 포인터가 무효화될 수 있음.
    // 요소의 인덱스만 보관하고 변경 후 다시 접근함.
    samples.push_back(30);

    if (index < samples.size()) {
        std::println("Sample: {}", samples[index]);
    }
    std::println("Count: {}", samples.size());
}
