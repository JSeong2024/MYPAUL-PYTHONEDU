#include <format>
#include <print>
#include <string>
#include <type_traits>
#include <variant>

struct Temperature { double celsius; };
struct Battery { int percent; };

using Reading = std::variant<Temperature, Battery>;

[[nodiscard]] std::string describe(const Reading& reading) {
    return std::visit([](const auto& item) -> std::string {
        using T = std::decay_t<decltype(item)>;
        if constexpr (std::is_same_v<T, Temperature>) {
            return std::format("Temperature: {:.1f} C", item.celsius);
        } else {
            return std::format("Battery: {}%", item.percent);
        }
    }, reading);
}

int main() {
    const Reading first{Temperature{23.5}};
    const Reading second{Battery{87}};
    std::println("{}", describe(first));
    std::println("{}", describe(second));
}
