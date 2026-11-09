#include <iostream>
#include <string>
#include <string_view>
int main() {
    const std::string_view chunks[]{"HEL", "LO|WOR", "LD|"};
    std::string pending;
    int messages = 0;
    for (const auto chunk : chunks) {
        pending.append(chunk);
        for (std::size_t split; (split = pending.find('|')) != std::string::npos;) {
            std::cout << "Message: " << pending.substr(0, split) << '\n';
            pending.erase(0, split + 1);
            ++messages;
        }
    }
    std::cout << "Count: " << messages << '\n';
}
