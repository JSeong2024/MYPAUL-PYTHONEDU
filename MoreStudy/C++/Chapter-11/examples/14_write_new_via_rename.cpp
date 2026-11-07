#include <filesystem>
#include <fstream>
#include <print>
#include <string_view>
#include <system_error>

// 신규 파일 생성 예제. 동시 접근·신뢰할 수 없는 디렉터리에는 적합하지 않음.
[[nodiscard]] bool save_new(const std::filesystem::path& destination,
                            std::string_view content) {
    namespace fs = std::filesystem;
    std::error_code ec;
    if (fs::exists(destination, ec) || ec) return false; // 덮어쓰기 금지
    fs::path temporary = destination;
    temporary += ".tmp";
    if (fs::exists(temporary, ec) || ec) return false;
    {
        std::ofstream output{temporary, std::ios::binary | std::ios::trunc};
        if (!output) return false;
        output.write(content.data(), static_cast<std::streamsize>(content.size()));
        output.close();
        if (!output) {
            fs::remove(temporary, ec);
            return false;
        }
    }
    fs::rename(temporary, destination, ec);
    if (ec) {
        std::error_code cleanup_error;
        fs::remove(temporary, cleanup_error);
        return false;
    }
    return true;
}

int main(int argc, char* argv[]) {
    if (argc != 2) return 1;
    if (!save_new(argv[1], "mode=automatic\n")) {
        std::println(stderr, "Save failed (target or temporary file may exist)");
        return 1;
    }
    std::println("Created new file");
}
