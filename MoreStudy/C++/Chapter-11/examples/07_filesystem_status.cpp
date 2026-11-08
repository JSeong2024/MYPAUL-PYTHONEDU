#include <filesystem>
#include <iostream>
#include <system_error>
int main(int argc, char* argv[]) {
    if (argc != 2) { std::cerr << "Usage: filesystem_status <path>\n"; return 1; }
    std::error_code ec;
    const bool exists = std::filesystem::exists(argv[1],ec);
    if (ec) { std::cerr << "Status error: " << ec.message() << '\n'; return 1; }
    std::cout << std::boolalpha << "Exists: " << exists << '\n';
}
