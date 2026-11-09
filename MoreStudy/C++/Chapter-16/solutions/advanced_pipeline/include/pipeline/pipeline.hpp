#pragma once
#include <cstddef>
#include <iosfwd>
#include <map>
#include <string>
#include <vector>

namespace pipeline {
struct Reading { std::string id; int value{}; bool valid{}; };
struct Parsed { std::vector<Reading> rows; std::size_t rejected{}; };
struct Summary { std::size_t count{}; int total{}; std::size_t alerts{}; };
[[nodiscard]] Parsed parse_csv(std::istream& input);
[[nodiscard]] std::map<std::string, Summary> summarize(const std::vector<Reading>& rows, int threshold);
}
