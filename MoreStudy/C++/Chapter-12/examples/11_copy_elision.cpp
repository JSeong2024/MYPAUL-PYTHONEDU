#include <iostream>

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
    return Token{id}; // 같은 타입 prvalue: C++17부터 직접 구성 보장
}

int main() {
    Token token = make_token(27);
    std::cout << "Token: " << token.id() << '\n';
}
