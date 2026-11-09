#pragma once
#include <span>
#include <cstddef>
namespace device {
[[nodiscard]] bool is_valid(int value) noexcept;
[[nodiscard]] std::size_t count_valid(std::span<const int> values) noexcept;
}
