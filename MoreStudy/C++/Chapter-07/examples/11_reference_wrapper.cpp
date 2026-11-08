#include <functional>
#include <iostream>
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
    std::cout << "Front: " << front_rpm << '\n';
    std::cout << "Rear: " << rear_rpm << '\n';
}
