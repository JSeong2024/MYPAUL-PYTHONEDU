#include <fstream>
#include <print>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::println(stderr, "Usage: append_log <path>");
        return 1;
    }
    std::ofstream output{argv[1], std::ios::app};
    if (!output) {
        std::println(stderr, "Cannot open log file");
        return 1;
    }
    output << "INFO|robot-01|heartbeat\n";
    output.close();
    if (!output) {
        std::println(stderr, "Append failed");
        return 1;
    }
    std::println("Log appended");
}
