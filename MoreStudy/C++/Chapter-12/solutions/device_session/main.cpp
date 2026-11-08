#include "session.hpp"
#include <iostream>
#include <utility>
#include <variant>

int main() {
    {
        auto result = demo::Session::open("sensor-A");
        if (std::holds_alternative<demo::OpenError>(result)) {
            std::cerr << "Open failed\n";
            return 1;
        }
        demo::Session session{std::move(std::get<demo::Session>(result))};
        std::cout << "Connected: " << session.name() << '\n';
        std::cout << "Samples: " << session.next_reading() << ", "
                  << session.next_reading() << ", " << session.next_reading() << '\n';
    }
    std::cout << "Closed sessions: " << demo::closed_count() << '\n';
    auto rejected = demo::Session::open("");
    if (auto* error = std::get_if<demo::OpenError>(&rejected)) {
        std::cout << "Rejected: " << demo::error_message(*error) << '\n';
    }
}
