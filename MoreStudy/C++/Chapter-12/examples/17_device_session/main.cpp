#include "session.hpp"
#include <print>
#include <utility>

int main() {
    {
        auto result = demo::Session::open("sensor-A");
        if (!result) {
            std::println(stderr, "Error: {}", result.error());
            return 1;
        }
        demo::Session session{std::move(*result)};
        std::println("Connected: {}", session.name());
        const int first = session.next_reading();
        const int second = session.next_reading();
        const int third = session.next_reading();
        std::println("Samples: {}, {}, {}", first, second, third);
    }
    std::println("Closed sessions: {}", demo::closed_count());
    auto rejected = demo::Session::open("");
    if (!rejected) std::println("Rejected: {}", rejected.error());
}
