#include <cstdint>
#include <fstream>
#include <print>
#include <string>

int main(int argc, char* argv[]) {
    if (argc != 2) return 1;
    std::ifstream input{argv[1]};
    if (!input) return 1;
    std::uint64_t bytes{};
    std::uint64_t lines{};
    std::string line;
    while (std::getline(input, line)) {
        ++lines;
        bytes += line.size(); // 개행 바이트는 제외한 데이터 크기
    }
    if (input.bad()) return 1;
    std::println("Lines: {}, payload bytes: {}", lines, bytes);
}
