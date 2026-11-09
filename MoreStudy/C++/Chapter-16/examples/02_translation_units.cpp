#include <iostream>
#include <string_view>

int count_tokens(std::string_view text) {
    int count = 0;
    bool inside = false;
    for (char ch : text) {
        if (ch == ' ') { inside = false; }
        else if (!inside) { inside = true; ++count; }
    }
    return count;
}
int main() {
    std::cout << "Tokens: " << count_tokens("CMake builds targets") << '\n';
}
