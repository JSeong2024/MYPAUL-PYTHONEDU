#include <charconv>
#include <cstdint>
#include <fstream>
#include <map>
#include <print>
#include <string>
#include <string_view>

[[nodiscard]] bool valid_id(std::string_view id) {
    if (id.empty() || id.size() > 32) return false;
    for (const unsigned char c : id) {
        if (!((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') ||
              (c >= '0' && c <= '9') || c == '_' || c == '-')) return false;
    }
    return true;
}

int main(int argc, char* argv[]) {
    if (argc != 2) return 1;
    std::ifstream input{argv[1]};
    if (!input) return 1;
    std::string line;
    if (!std::getline(input, line)) return 1;
    if (!line.empty() && line.back() == '\r') line.pop_back();
    if (line != "id,quantity") return 1;
    std::map<std::string, int> inventory;
    std::uint64_t total{};
    while (std::getline(input, line)) {
        if (!line.empty() && line.back() == '\r') line.pop_back();
        const auto comma = line.find(',');
        if (comma == std::string::npos || line.find(',', comma + 1) != std::string::npos) return 1;
        const std::string_view id{line.data(), comma};
        const std::string_view quantity_text{line.data() + comma + 1, line.size() - comma - 1};
        if (!valid_id(id) || quantity_text.empty()) return 1;
        int quantity{};
        const auto [end, error] = std::from_chars(quantity_text.data(),
                                                quantity_text.data() + quantity_text.size(), quantity);
        if (error != std::errc{} || end != quantity_text.data() + quantity_text.size() ||
            quantity < 0 || quantity > 1'000'000) return 1;
        if (!inventory.emplace(std::string{id}, quantity).second) return 1;
        total += static_cast<std::uint64_t>(quantity);
    }
    if (input.bad()) return 1;
    for (const auto& [id, quantity] : inventory) {
        std::println("{}: {}", id, quantity);
    }
    std::println("Total: {}", total);
}
