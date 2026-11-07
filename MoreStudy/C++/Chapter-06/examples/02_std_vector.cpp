#include <print>
#include <vector>

int main() {
    std::vector<int> samples;
    samples.reserve(4);  // 용량 예약. 아직 요소는 없음.

    for (const int value : {12, 15, 13, 18}) {
        samples.push_back(value);
    }

    std::println("Size: {}", samples.size());
    for (const int sample : samples) {
        std::println("Reading: {}", sample);
    }
}
