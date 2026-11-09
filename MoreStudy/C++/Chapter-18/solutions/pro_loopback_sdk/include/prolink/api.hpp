#pragma once
#include <optional>
#include <string>
#include <string_view>
namespace prolink {
enum class Error { none, invalid_request, too_large, transport };
struct Result {
    std::string reply;
    Error error{Error::none};
    [[nodiscard]] explicit operator bool() const noexcept { return error == Error::none; }
};
[[nodiscard]] std::string process_command(std::string_view command);
[[nodiscard]] std::optional<std::string> decode_packet(std::string_view packet);
[[nodiscard]] Result round_trip(std::string_view command);
} // namespace prolink
