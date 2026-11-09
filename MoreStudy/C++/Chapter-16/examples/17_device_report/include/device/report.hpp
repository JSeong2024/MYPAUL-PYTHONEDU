#pragma once
#include <cstddef>
#include <span>
#include <string>

namespace device {
struct Record { std::string id; int reading{}; };
struct Summary { std::size_t count{}; std::size_t alerts{}; int total{}; };
[[nodiscard]] Summary summarize(std::span<const Record> records, int threshold);
}
