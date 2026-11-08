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
    [[nodiscard]] const std::vector<std::string>& messages() const noexcept { return messages_; }
private:
    std::vector<std::string> messages_;
};
[[nodiscard]] bool report_fault(Transport& transport, int code) {
    // TODO: code가 양수이면 "FAULT:<code>"를 전송하고 전송 성공 여부를 반환하세요.
    (void)transport;
    (void)code;
    return false;
}
int main() {
    FakeTransport fake;
    const bool sent = report_fault(fake, 42);
    const bool rejected = report_fault(fake, 0);
    std::cout << std::boolalpha << "Sent: " << sent << ", rejected: "
              << rejected << ", messages: " << fake.messages().size() << '\n';
}
