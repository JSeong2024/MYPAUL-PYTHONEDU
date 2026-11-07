#include <print>

int main() {
    int speed{120};
    int backup{80};

    const int* read_only{&speed};
    read_only = &backup;  // 다른 객체를 가리킬 수 있음

    int* const fixed_target{&speed};
    *fixed_target = 130; // 가리키는 값은 수정 가능

    const int* const fixed_read_only{&speed};

    std::println("Backup: {}", *read_only);
    std::println("Speed: {}", *fixed_target);
    std::println("Read-only speed: {}", *fixed_read_only);
}
