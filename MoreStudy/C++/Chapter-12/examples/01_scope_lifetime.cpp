#include <print>
#include <string_view>

class Trace {
public:
    explicit Trace(std::string_view name) : name_(name) {
        std::println("Open: {}", name_);
    }
    ~Trace() { std::println("Close: {}", name_); }
    Trace(const Trace&) = delete;
    Trace& operator=(const Trace&) = delete;
private:
    std::string_view name_;  // 호출 중 유효한 문자열 리터럴을 참조
};

int main() {
    Trace outer{"outer"};
    {
        Trace inner{"inner"};
        std::println("Working");
    }
    std::println("End of main");
}
