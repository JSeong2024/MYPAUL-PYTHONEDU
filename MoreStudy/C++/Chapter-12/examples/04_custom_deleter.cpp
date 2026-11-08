#include <cstdio>
#include <iostream>
#include <memory>

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
        std::cerr << "Cannot create temporary file\n";
        return 1;
    }
    if (std::fputs("sample=42\n", file.get()) < 0 || std::fflush(file.get()) != 0) {
        std::cerr << "Write failed\n";
        return 1;
    }
    std::cout << "Temporary file written\n";
}
