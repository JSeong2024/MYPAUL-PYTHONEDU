#include <iostream>
#include <print>
#include <vector>

int main() {
    // 입력: N(1~1000), 이어서 N개의 정수(-1000000~1000000)
    int count{};
    if (!(std::cin >> count) || count < 1 || count > 1'000) {
        std::println(stderr, "Invalid sample count");
        return 1;
    }

    std::vector<int> samples;
    samples.reserve(static_cast<std::size_t>(count));

    // TODO: 모든 센서 값을 읽고 유효 범위를 검증함.
    // TODO: 최솟값, 최댓값, 평균을 계산함.
    // 출력: Count / Min / Max / Average (소수 둘째 자리)
    std::println("TODO: implement sensor statistics");
}
