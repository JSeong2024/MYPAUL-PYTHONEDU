#include <algorithm>
#include <print>

class RetryPolicy {
public:
    RetryPolicy() : RetryPolicy(3, 250) {}

    RetryPolicy(int attempts, int delay_ms) noexcept
        : attempts_{std::clamp(attempts, 1, 10)},
          delay_ms_{std::clamp(delay_ms, 0, 5'000)} {}

    [[nodiscard]] int attempts() const noexcept { return attempts_; }
    [[nodiscard]] int delay_ms() const noexcept { return delay_ms_; }

private:
    int attempts_{};
    int delay_ms_{};
};

int main() {
    const RetryPolicy defaults;
    const RetryPolicy custom{20, 600};
    std::println("Default: {} times, {} ms", defaults.attempts(), defaults.delay_ms());
    std::println("Custom: {} times, {} ms", custom.attempts(), custom.delay_ms());
}
