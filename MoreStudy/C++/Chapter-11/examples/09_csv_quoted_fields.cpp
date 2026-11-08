#include <iostream>
#include <string>
#include <vector>
std::vector<std::string> split_csv(const std::string& line) {
    std::vector<std::string> fields;
    std::string field;
    bool quoted{};
    for (std::size_t i{}; i < line.size(); ++i) {
        const char c = line[i];
        if (c == '"') {
            if (quoted && i+1 < line.size() && line[i+1] == '"') { field += '"'; ++i; }
            else { quoted = !quoted; }
        } else if (c == ',' && !quoted) { fields.push_back(field); field.clear(); }
        else { field += c; }
    }
    if (quoted) { return {}; }
    fields.push_back(field);
    return fields;
}
int main() {
    const auto fields = split_csv("SENSOR-A,\"north, west\",23");
    if (fields.size() != 3) { return 1; }
    std::cout << "Location: " << fields[1] << '\n';
}
