#include <iostream>

int main() {
    int speed{120};
    int backup{80};
    const int* read_only{&speed};
    read_only = &backup;
    int* const fixed_target{&speed};
    *fixed_target = 130;
    const int* const fixed_read_only{&speed};

    std::cout << "Backup: " << *read_only << '\n';
    std::cout << "Speed: " << *fixed_target << '\n';
    std::cout << "Read-only speed: " << *fixed_read_only << '\n';
}
