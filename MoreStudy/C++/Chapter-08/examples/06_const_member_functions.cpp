#include <iostream>

class SampleCounter {
public:
    void record() noexcept { ++count_; }
    [[nodiscard]] int count() const noexcept { return count_; }

private:
    int count_{};
};

void print_count(const SampleCounter& counter) {
    std::cout << "Samples: " << counter.count() << '\n';
}

int main() {
    SampleCounter counter;
    counter.record();
    counter.record();
    print_count(counter);
}
