#include "pipeline/pipeline.hpp"
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

int main() {
    std::istringstream input{"A,20,ok\nB,91,ok\nA,40,bad\nA,70,ok\nBROKEN,abc,ok\nB,8,ok\n"};
    const auto parsed = pipeline::parse_csv(input);
    if (parsed.rows.size() != 5 || parsed.rejected != 1) return 1;
    const auto result = pipeline::summarize(parsed.rows, 80);
    if (result.size() != 2 || result.at("A").count != 2 || result.at("A").total != 90 ||
        result.at("B").alerts != 1 || result.at("B").total != 99) return 2;
    std::istringstream bad{"\nA,101,ok\nA,2,unknown\nA,2,ok,extra\n"};
    const auto invalid = pipeline::parse_csv(bad);
    if (invalid.rejected != 4 || !invalid.rows.empty()) return 3;
    std::istringstream windows{"C,42,ok\r\n"};
    if (pipeline::parse_csv(windows).rows.size() != 1) return 4;
    if (!pipeline::summarize(std::vector<pipeline::Reading>{}, 80).empty()) return 5;
    bool thrown = false;
    try { (void)pipeline::summarize(parsed.rows, -1); }
    catch (const std::invalid_argument&) { thrown = true; }
    return thrown ? 0 : 6;
}
