#include <print>

class SampleCounter {
public:
    void record() noexcept { ++count_; }
    [[nodiscard]] int count() const noexcept { return count_; }

private:
    int count_{};
};

void print_count(const SampleCounter& counter) {
    std::println("Samples: {}", counter.count());
}

int main() {
    SampleCounter counter;
    counter.record();
    counter.record();
    print_count(counter);
}
