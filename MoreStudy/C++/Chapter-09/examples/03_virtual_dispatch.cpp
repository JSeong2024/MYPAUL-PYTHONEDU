#include <print>
#include <string_view>

class StatusSource {
public:
    virtual ~StatusSource() = default;
    [[nodiscard]] virtual std::string_view status() const noexcept {
        return "unknown";
    }
};

class OnlineSensor final : public StatusSource {
public:
    [[nodiscard]] std::string_view status() const noexcept override {
        return "online";
    }
};

void report(const StatusSource& source) {
    std::println("Sensor status: {}", source.status());
}

int main() {
    const OnlineSensor sensor;
    report(sensor);  // 기반 클래스 참조로 전달
}
