#include <iostream>
#include <string>
#include <string_view>

[[nodiscard]] bool split_record(std::string_view text,
                                std::string_view& device,
                                std::string_view& status) {
    const auto separator = text.find('|');
    if (separator == std::string_view::npos || separator == 0 ||
        separator + 1 == text.size() || text.find('|', separator + 1) != std::string_view::npos) {
        return false;
    }
    device = text.substr(0, separator);
    status = text.substr(separator + 1);
    return true;
}

int main() {
    for (const std::string_view record : {"ROOM-01|OK", "ROOM-02|WARN|EXTRA"}) {
        std::string_view device;
        std::string_view status;
        if (split_record(record, device, status)) {
            std::cout << device << ": " << status << '\n';
        } else {
            std::cout << "Rejected: " << record << '\n';
        }
    }
}
