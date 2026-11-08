#include "session.hpp"
#include <stdexcept>
#include <string>
#include <utility>

namespace demo {
struct RawPort { std::string id; int index{0}; };
namespace {
int closed{};
[[nodiscard]] RawPort* open_port(std::string_view id) {
    // 실제 장치 SDK 대신 새 자원을 생성하는 테스트용 구현입니다.
    return new RawPort{std::string{id}};
}
}
void close_port(RawPort* port) noexcept {
    if (port != nullptr) {
        delete port;
        ++closed;
    }
}
int closed_count() noexcept { return closed; }
std::string_view error_message(OpenError error) noexcept {
    switch (error) {
    case OpenError::empty_id: return "empty id";
    case OpenError::unavailable: return "device unavailable";
    }
    return "unknown error";
}
void Session::Closer::operator()(RawPort* port) const noexcept { close_port(port); }
std::variant<Session, OpenError> Session::open(std::string_view id) {
    if (id.empty()) return OpenError::empty_id;
    if (id == "offline") return OpenError::unavailable;
    return Session{open_port(id)};
}
int Session::next_reading() {
    if (!port_) throw std::logic_error("session does not own a port");
    constexpr int values[]{21, 24, 22};
    const int reading = values[port_->index % 3];
    ++port_->index;
    return reading;
}
std::string_view Session::name() const noexcept {
    return port_ ? std::string_view{port_->id} : std::string_view{};
}
} // namespace demo
