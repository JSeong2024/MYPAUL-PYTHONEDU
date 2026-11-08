#include <iostream>
#include <string>
#include <utility>

void inspect(const std::string&) { std::cout << "Lvalue\n"; }
void inspect(std::string&&) { std::cout << "Rvalue\n"; }

int main() {
    std::string text{"abc"};
    inspect(text);
    inspect(std::move(text));
    std::string&& named_reference = std::string{"temporary"};
    inspect(named_reference); // 이름을 가진 rvalue 참조 표현식은 lvalue
}
