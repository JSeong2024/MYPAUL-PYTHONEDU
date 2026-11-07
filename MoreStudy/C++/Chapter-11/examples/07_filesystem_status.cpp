#include <filesystem>
#include <print>
#include <system_error>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::println(stderr, "Usage: filesystem_status <path>");
        return 1;
    }
    namespace fs = std::filesystem;
    const fs::path path{argv[1]};
    std::error_code ec;
    const fs::file_status status = fs::status(path, ec);
    if (ec) {
        std::println(stderr, "Status failed: {}", ec.message());
        return 1;
    }
    if (!fs::is_regular_file(status)) {
        std::println(stderr, "Not a regular file");
        return 1;
    }
    const auto size = fs::file_size(path, ec);
    if (ec) {
        std::println(stderr, "Size failed: {}", ec.message());
        return 1;
    }
    std::println("Size: {} bytes", size);
}
