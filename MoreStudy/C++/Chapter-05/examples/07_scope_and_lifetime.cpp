#include <iostream>

int next_attempt(int current) {
    const int updated{current + 1};
    return updated;
}

int main() {
    int attempt{1};
    {
        const int local_bonus{2};
        attempt += local_bonus;
    }
    std::cout << "Attempt: " << next_attempt(attempt) << '\n';
}
