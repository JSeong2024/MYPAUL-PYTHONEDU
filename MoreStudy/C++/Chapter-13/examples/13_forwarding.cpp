#include <concepts>
#include <print>
#include <string>
#include <utility>
#include <vector>

struct Event {
    std::string source;
    int code;
    Event(std::string src, int value) : source(std::move(src)), code(value) {}
};

class EventBuffer {
public:
    template <typename... Args>
        requires std::constructible_from<Event, Args...>
    Event& append(Args&&... args) {
        // 검증 정책이 있는 저장 API를 제공; 생성은 vector::emplace_back에 위임.
        return events_.emplace_back(std::forward<Args>(args)...);
    }
    [[nodiscard]] const std::vector<Event>& events() const noexcept { return events_; }
private:
    std::vector<Event> events_;
};

int main() {
    EventBuffer buffer;
    std::string device{"sensor-A"};
    buffer.append(device, 200);     // 문자열 복사
    buffer.append("camera-B", 201); // 임시 문자열 생성
    std::println("Events: {}", buffer.events().size());
    std::println("First source: {}", buffer.events().front().source);
}
