#include "session.hpp"
#include <stdexcept>
#include <string>

namespace demo {
struct RawPort { std::string id; int index{0}; };
namespace { int closed{}; }

void close_port(RawPort* port) noexcept {
    // TODO 1: port가 있다면 delete로 해제하고 closed를 증가시킵니다.
    (void)port;
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
    // TODO 2: 빈 id와 "offline"을 구분해 오류를 반환합니다.
    // TODO 3: 유효한 id면 new RawPort{std::string{id}}를 소유한 Session을 반환합니다.
    (void)id;
    return OpenError::unavailable;
}
int Session::next_reading() {
    // TODO 4: 소유권이 없는 상태면 std::logic_error 발생
    // TODO 5: 순서대로 21, 24, 22를 순환하며 반환
    throw std::logic_error("not implemented");
}
std::string_view Session::name() const noexcept {
    return port_ ? std::string_view{port_->id} : std::string_view{};
}
} // namespace demo
