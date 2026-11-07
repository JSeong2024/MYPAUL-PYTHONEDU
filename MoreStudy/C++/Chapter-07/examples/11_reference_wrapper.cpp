#include <functional>
#include <print>
#include <vector>

int main() {
    int front_rpm{1'000};
    int rear_rpm{1'200};

    std::vector<std::reference_wrapper<int>> motors{
        std::ref(front_rpm), std::ref(rear_rpm)
    };
    for (int& rpm : motors) {
        rpm += 100;
    }

    std::println("Front: {}", front_rpm);
    std::println("Rear: {}", rear_rpm);
}
