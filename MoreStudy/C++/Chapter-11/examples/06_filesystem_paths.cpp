#include <filesystem>
#include <print>

int main() {
    namespace fs = std::filesystem;
    const fs::path file = fs::path{"data"} / "logs" / "robot.csv";
    std::println("File name: {}", file.filename().string());
    std::println("Extension: {}", file.extension().string());
    std::println("Parent: {}", file.parent_path().generic_string());
}
