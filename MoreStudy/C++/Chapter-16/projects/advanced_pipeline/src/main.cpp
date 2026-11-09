#include "pipeline/pipeline.hpp"
#include <fstream>
#include <iostream>
#include <stdexcept>

int main(int argc, char** argv) {
    if (argc != 2) { std::cerr << "Usage: pipeline_cli <data.csv>\n"; return 2; }
    std::ifstream input{argv[1]};
    if (!input) { std::cerr << "Error: cannot open CSV\n"; return 2; }
    try {
        const auto parsed = pipeline::parse_csv(input);
        const auto summary = pipeline::summarize(parsed.rows, 80);
        std::size_t accepted{};
        for (const auto& [id, item] : summary) { (void)id; accepted += item.count; }
        std::cout << "accepted=" << accepted << " rejected=" << parsed.rejected << '\n';
        for (const auto& [id, item] : summary)
            std::cout << id << ' ' << item.count << ' ' << item.total << ' ' << item.alerts << '\n';
    } catch (const std::exception& error) {
        std::cerr << "Error: " << error.what() << '\n'; return 1;
    }
}
