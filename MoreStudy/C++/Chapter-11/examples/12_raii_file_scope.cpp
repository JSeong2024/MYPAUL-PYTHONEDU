#include <fstream>
#include <print>
#include <string>

[[nodiscard]] bool save_message(const char* path, const std::string& message) {
    std::ofstream output{path, std::ios::trunc};
    if (!output) return false;
    output << message << '\n';
    output.close();
    return output.good();
}

int main(int argc, char* argv[]) {
    if (argc != 2) return 1;
    if (!save_message(argv[1], "status=ready")) {
        std::println(stderr, "Save failed");
        return 1;
    }
    std::println("Saved");
}
