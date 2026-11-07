#include <print>

int main() {
    constexpr int response_time_ms{180};
    constexpr int slow_threshold_ms{200};

    const char* label = response_time_ms > slow_threshold_ms
                            ? "SLOW"
                            : "NORMAL";

    std::println("Response: {} ms ({})", response_time_ms, label);
}
