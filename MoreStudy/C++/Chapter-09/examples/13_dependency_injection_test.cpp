#include <print>
#include <string>
#include <string_view>
#include <vector>

class ITransport {
public:
    virtual ~ITransport() = default;
    virtual bool send(std::string_view message) = 0;
};

class FakeTransport final : public ITransport {
public:
    bool send(std::string_view message) override {
        messages_.emplace_back(message);
        return true;
    }
    [[nodiscard]] const std::vector<std::string>& messages() const noexcept {
        return messages_;
    }

private:
    std::vector<std::string> messages_;
};

[[nodiscard]] bool send_alarm(ITransport& transport, std::string_view text) {
    return !text.empty() && transport.send(text);
}

int main() {
    FakeTransport fake;
    const bool sent = send_alarm(fake, "OVERHEAT");
    const bool correct = sent && fake.messages().size() == 1 &&
                         fake.messages().front() == "OVERHEAT";
    std::println("Transport test: {}", correct ? "PASS" : "FAIL");
    return correct ? 0 : 1;
}
