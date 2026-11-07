#include "session.hpp"
#include <memory>
#include <stdexcept>
#include <string>

namespace demo {
struct RawPort {
    std::string id;
    int index{0};
};

namespace {
int closed{};
[[nodiscard]] RawPort* open_port(std::string_view id) {
    return new RawPort{std::string{id}}; // 외부 C API를 흉내 낸 코드
}
}
void close_port(RawPort* port) noexcept {
    if (port != nullptr) {
        delete port;
        ++closed;
    }
}
int closed_count() noexcept { return closed; }
void Session::Closer::operator()(RawPort* port) const noexcept { close_port(port); }

std::expected<Session, std::string> Session::open(std::string_view id) {
    if (id.empty()) return std::unexpected("device id is empty");
    return Session{open_port(id)};
}
int Session::next_reading() {
    if (!port_) throw std::logic_error("session is moved from");
    constexpr int values[]{21, 24, 22};
    const int index = port_->index++;
    return values[index % 3];
}
std::string_view Session::name() const noexcept {
    return port_ ? std::string_view{port_->id} : std::string_view{};
}
} // namespace demo
