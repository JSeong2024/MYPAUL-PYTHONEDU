#include <iostream>
#include <stdexcept>
struct Clock { virtual ~Clock() = default; virtual int tick() const = 0; };
struct FixedClock final : Clock { int tick() const override { return 120; } };
bool expired(const Clock& clock,int deadline) { return clock.tick() >= deadline; }
int main() {
    FixedClock clock;
    if (!expired(clock,100) || expired(clock,130)) throw std::runtime_error("clock");
    std::cout << "Clock tests: PASS\n";
}
