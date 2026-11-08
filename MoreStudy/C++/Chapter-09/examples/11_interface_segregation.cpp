#include <iostream>

class Reader {
public:
    virtual ~Reader() = default;
    [[nodiscard]] virtual int read() const noexcept = 0;
};
class Resettable {
public:
    virtual ~Resettable() = default;
    virtual void reset() noexcept = 0;
};
class CounterSensor final : public Reader, public Resettable {
public:
    [[nodiscard]] int read() const noexcept override { return count_; }
    void reset() noexcept override { count_ = 0; }
    void tick() noexcept { ++count_; }
private:
    int count_{};
};
int main() {
    CounterSensor counter;
    counter.tick();
    const Reader& reader = counter;
    Resettable& control = counter;
    std::cout << "Before: " << reader.read() << '\n';
    control.reset();
    std::cout << "After: " << reader.read() << '\n';
}
