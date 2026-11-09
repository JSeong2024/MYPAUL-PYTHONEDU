#include <cstddef>
#include <optional>
// nullptr가 아닌 소스에서 max_samples회 읽어 경보 이상 값 개수 반환.
// nullopt 값은 결측으로 취급, 경보 조건은 reading >= threshold.
struct ReadingSource {
    virtual ~ReadingSource() = default;
    virtual std::optional<int> next() = 0;
};
std::size_t count_alerts(ReadingSource& source, std::size_t max_samples, int threshold) {
    // TODO: 고정된 Fake Source로 테스트 가능한 집계 함수 구현
    (void)source; (void)max_samples; (void)threshold;
    return 0;
}
#ifndef CH17_LIBRARY_ONLY
#include <iostream>
int main(){std::cout << "count_alerts: TODO\n";}
#endif
