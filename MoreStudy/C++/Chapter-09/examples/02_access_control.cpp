#include <print>
#include <string>
#include <string_view>
#include <utility>

class Controller {
public:
    explicit Controller(std::string name) : name_(std::move(name)) {}
    [[nodiscard]] std::string_view name() const noexcept { return name_; }
    [[nodiscard]] bool enabled() const noexcept { return enabled_; }

protected:
    void set_enabled(bool value) noexcept { enabled_ = value; }

private:
    std::string name_;
    bool enabled_{false};
};

class FanController final : public Controller {
public:
    using Controller::Controller;
    void start() noexcept { set_enabled(true); }
    void stop() noexcept { set_enabled(false); }
};

int main() {
    FanController fan{"Fan-A"};
    fan.start();
    std::println("{} enabled: {}", fan.name(), fan.enabled());
}
