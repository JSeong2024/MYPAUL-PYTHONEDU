#include "report.hpp"
#include <filesystem>
#include <print>
#include <system_error>

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::println(stderr, "Usage: sensor_report <input.csv> <output.txt>");
        return 1;
    }
    namespace fs = std::filesystem;
    const fs::path input{argv[1]};
    const fs::path output{argv[2]};
    std::error_code ec;
    if (fs::exists(output, ec)) {
        if (fs::equivalent(input, output, ec) && !ec) {
            std::println(stderr, "Input and output must be different files");
            return 1;
        }
    } else if (ec) {
        std::println(stderr, "Output path check failed: {}", ec.message());
        return 1;
    }
    const auto report = build_report(input);
    if (!report) {
        std::println(stderr, "{}", report.error());
        return 1;
    }
    if (const auto result = write_report(output, *report); !result) {
        std::println(stderr, "{}", result.error());
        return 1;
    }
    std::println("Saved report: {} readings from {} devices",
                 report->samples, report->counts.size());
}
