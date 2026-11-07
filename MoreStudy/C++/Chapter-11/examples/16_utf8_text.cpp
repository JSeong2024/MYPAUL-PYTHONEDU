#include <fstream>
#include <print>
#include <string>

int main(int argc, char* argv[]) {
    if (argc != 2) return 1;
    const std::string value = "센서"; // 소스 파일을 UTF-8로 저장
    std::ofstream output{argv[1], std::ios::binary | std::ios::trunc};
    if (!output) return 1;
    output.write(value.data(), static_cast<std::streamsize>(value.size()));
    output.close();
    if (!output) return 1;
    std::println("UTF-8 bytes: {}", value.size());
}
