#include <filesystem>
#include <iostream>
int main() {
    const std::filesystem::path path = std::filesystem::path{"reports"} / "daily" / "result.csv";
    std::cout << "Filename: " << path.filename().string() << '\n';
    std::cout << "Extension: " << path.extension().string() << '\n';
}
