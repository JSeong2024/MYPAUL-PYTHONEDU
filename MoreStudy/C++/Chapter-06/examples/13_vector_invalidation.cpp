#include <print>
#include <vector>

int main() {
    std::vector<int> readings{10, 20};
    const std::size_t selected_index{1};

    // push_back 중 재할당이 발생하면 이전 요소의 참조·포인터가 무효화될 수 있음.
    readings.push_back(30);

    // 저장해 둔 참조 대신, 유효 범위를 확인한 인덱스로 다시 접근함.
    if (selected_index < readings.size()) {
        std::println("Selected reading: {}", readings.at(selected_index));
    }
}
