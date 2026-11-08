#include <iomanip>
#include <iostream>

int main() {
    int sample_count{};
    std::cout << "Samples (1-6): " << std::flush;
    if (!(std::cin >> sample_count) ||
        sample_count < 1 || sample_count > 6) {
        std::cerr << "Error: sample count must be between 1 and 6.\n";
        return 1;
    }

    // TODO: 각 측정값을 최대 두 번까지 입력받습니다.
    // TODO: 허용 범위는 0~100이며, 잘못된 정수 범위는 재시도합니다.
    // TODO: 정수 변환 실패는 즉시 오류 종료합니다.
    // TODO: 재시도 모두 실패하면 오류 종료합니다.
    // TODO: 합계, 평균, 최솟값, 최댓값, 80 이상인 측정값 수를 출력합니다.
    return 0;
}
