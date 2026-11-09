#include <iostream>
#include <string>
#include <string_view>
[[nodiscard]] std::string process(std::string_view request) {
    if (request == "PING") return "PONG";
    if (request == "STATUS") return "READY";
    return "ERR unknown command";
}
int main() {
    std::cout << process("PING") << '\n' << process("STATUS") << '\n'
              << process("RESET") << '\n';
}
