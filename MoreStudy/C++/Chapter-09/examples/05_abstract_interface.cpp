#include <iostream>

class ReadingSource {
public:
    virtual ~ReadingSource() = default;
    [[nodiscard]] virtual int read() const noexcept = 0;
};

class FixedReading final : public ReadingSource {
public:
    explicit FixedReading(int value) : value_{value} {}
    [[nodiscard]] int read() const noexcept override { return value_; }
private:
    int value_{};
};

[[nodiscard]] bool is_critical(const ReadingSource& source) {
    return source.read() >= 80;
}

int main() {
    const FixedReading source{85};
    std::cout << std::boolalpha << "Critical: " << is_critical(source) << '\n';
}
