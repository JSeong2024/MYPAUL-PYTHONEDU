#include <print>

class Token {
public:
    explicit Token(int id) : id_(id) {}
    Token(const Token&) = delete;
    Token(Token&&) = delete;
    [[nodiscard]] int id() const noexcept { return id_; }
private:
    int id_;
};

[[nodiscard]] Token make_token(int id) {
    return Token{id}; // 같은 타입의 prvalue: C++17부터 직접 구성
}

int main() {
    Token value = make_token(27);
    std::println("Token: {}", value.id());
}
