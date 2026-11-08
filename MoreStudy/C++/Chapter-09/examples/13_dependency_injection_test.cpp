#include <iostream>
#include <string>
#include <string_view>
#include <vector>

class Transport {
public:
    virtual ~Transport() = default;
    virtual bool send(std::string_view text) = 0;
};
class FakeTransport final : public Transport {
public:
    bool send(std::string_view text) override {
        messages_.emplace_back(text);
        return true;
    }
    [[nodiscard]] const std::vector<std::string>& messages() const noexcept {
        return messages_;
    }
private:
    std::vector<std::string> messages_;
};
[[nodiscard]] bool send_alarm(Transport& transport, std::string_view message) {
    return !message.empty() && transport.send(message);
}
int main() {
    FakeTransport fake;
    const bool sent = send_alarm(fake, "OVERHEAT");
    const bool blocked = !send_alarm(fake, "");
    const bool correct = sent && blocked && fake.messages().size() == 1 &&
                         fake.messages().front() == "OVERHEAT";
    std::cout << "Transport test: " << (correct ? "PASS" : "FAIL") << '\n';
    return correct ? 0 : 1;
}
