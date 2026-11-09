#pragma once
#include <string>
#include <string_view>
namespace echo {
[[nodiscard]] std::string round_trip(std::string_view message);
}
