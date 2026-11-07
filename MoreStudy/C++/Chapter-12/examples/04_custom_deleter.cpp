#include <cstdio>
#include <memory>
#include <print>

struct FileCloser {
    void operator()(std::FILE* file) const noexcept {
        if (file != nullptr) {
            (void)std::fclose(file);
        }
    }
};

int main() {
    std::unique_ptr<std::FILE, FileCloser> file{std::tmpfile()};
    if (!file) {
        std::println(stderr, "Cannot create temporary file");
        return 1;
    }
    if (std::fputs("sample=42\n", file.get()) < 0 || std::fflush(file.get()) != 0) {
        std::println(stderr, "Write failed");
        return 1;
    }
    std::println("Temporary file written");
    // fclose 결과 검증·저장 내구성이 중요하면 별도의 명시적 처리 필요
}
