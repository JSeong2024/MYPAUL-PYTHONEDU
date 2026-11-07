#include <array>
#include <cstddef>
#include <print>
#include <string>
#include <type_traits>
#include <utility>

// 고정 데이터 윈도우: 측정값 N개를 배열로 보유.
template <typename T, std::size_t N>
struct Window {
    static_assert(N > 0);
    std::array<T, N> values{};
    [[nodiscard]] constexpr std::size_t size() const noexcept { return N; }
};

int main() {
    Window<int, 3> readings{{10, 20, 30}};
    std::pair device{std::string{"motor-A"}, 120}; // CTAD
    static_assert(std::is_same_v<decltype(device.second), int>);
    std::println("Window size: {}", readings.size());
    std::println("{}: {} RPM", device.first, device.second);
}
