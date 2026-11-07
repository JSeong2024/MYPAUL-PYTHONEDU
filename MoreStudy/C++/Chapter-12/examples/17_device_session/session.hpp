#pragma once
#include <expected>
#include <memory>
#include <string>
#include <string_view>

namespace demo {
struct RawPort;
void close_port(RawPort* port) noexcept;
[[nodiscard]] int closed_count() noexcept;

class Session {
public:
    Session(const Session&) = delete;
    Session& operator=(const Session&) = delete;
    Session(Session&&) noexcept = default;
    Session& operator=(Session&&) noexcept = default;
    ~Session() = default;

    [[nodiscard]] static std::expected<Session, std::string> open(std::string_view id);
    [[nodiscard]] int next_reading();
    [[nodiscard]] std::string_view name() const noexcept;

private:
    struct Closer { void operator()(RawPort* port) const noexcept; };
    std::unique_ptr<RawPort, Closer> port_;
    explicit Session(RawPort* port) noexcept : port_(port) {}
};
} // namespace demo
