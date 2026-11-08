#include <iostream>
#include <string_view>

class Trace {
public:
    explicit Trace(std::string_view name) : name_(name) {
        std::cout << "Open: " << name_ << '\n';
    }
    ~Trace() { std::cout << "Close: " << name_ << '\n'; }
    Trace(const Trace&) = delete;
    Trace& operator=(const Trace&) = delete;
private:
    std::string_view name_;
};

int main() {
    Trace outer{"outer"};
    {
        Trace inner{"inner"};
        std::cout << "Working\n";
    }
    std::cout << "End of main\n";
}
