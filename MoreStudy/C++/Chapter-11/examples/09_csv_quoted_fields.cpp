#include <fstream>
#include <print>
#include <string>
#include <string_view>
#include <vector>
#include <utility>

// 한 행을 파싱하는 예제. 필드 내부 줄바꿈은 지원하지 않음.
[[nodiscard]] bool parse_csv_line(std::string_view line, std::vector<std::string>& fields) {
    fields.clear();
    std::size_t i{};
    while (true) {
        std::string field;
        if (i < line.size() && line[i] == '"') {
            ++i;
            bool closed = false;
            while (i < line.size()) {
                if (line[i] == '"') {
                    if (i + 1 < line.size() && line[i + 1] == '"') {
                        field.push_back('"');
                        i += 2;
                    } else {
                        ++i;
                        closed = true;
                        break;
                    }
                } else {
                    field.push_back(line[i++]);
                }
            }
            if (!closed || (i < line.size() && line[i] != ',')) return false;
        } else {
            while (i < line.size() && line[i] != ',') {
                if (line[i] == '"') return false;
                field.push_back(line[i++]);
            }
        }
        fields.push_back(std::move(field));
        if (i == line.size()) return true;
        ++i; // 쉼표 건너뛰기
    }
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::println(stderr, "Usage: csv_quoted_fields <path>");
        return 1;
    }
    std::ifstream input{argv[1]};
    if (!input) return 1;
    std::string line;
    std::size_t line_number{};
    std::vector<std::string> fields;
    while (std::getline(input, line)) {
        ++line_number;
        if (!line.empty() && line.back() == '\r') line.pop_back();
        if (!parse_csv_line(line, fields)) {
            std::println(stderr, "Invalid CSV at line {}", line_number);
            return 1;
        }
        std::println("Line {} has {} fields", line_number, fields.size());
    }
    if (input.bad()) return 1;
}
