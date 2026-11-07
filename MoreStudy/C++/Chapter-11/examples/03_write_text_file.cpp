#include <fstream>
#include <print>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::println(stderr, "Usage: write_text_file <output-path>");
        return 1;
    }
    std::ofstream output{argv[1], std::ios::out | std::ios::trunc};
    if (!output) {
        std::println(stderr, "Cannot create output file");
        return 1;
    }
    output << "device,temperature_c\n";
    output << "robot-01,23\n";
    output.close();
    if (!output) {
        std::println(stderr, "Write or close failed");
        return 1;
    }
    std::println("File written");
}
