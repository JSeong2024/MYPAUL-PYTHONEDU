#include <print>
#include <string_view>

class IAlarmChannel {
public:
    virtual ~IAlarmChannel() = default;
    virtual void notify(std::string_view message) const = 0;
};

// TODO: ConsoleAlarm과 SilentAlarm을 구현합니다.
// ConsoleAlarm: "ALARM: <message>" 출력
// SilentAlarm: 출력하지 않음

int main() {
    std::println("TODO: implement two alarm channels");
}
