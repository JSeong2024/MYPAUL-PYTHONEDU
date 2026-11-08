#include <fstream>
#include <iostream>
#include <string>

int main() {
    std::string path;
    if (!std::getline(std::cin, path)) {
        std::cout << "OPEN_ERROR\n";
        return 0;
    }
    std::ifstream input(path);
    if (!input) {
        std::cout << "OPEN_ERROR\n";
        return 0;
    }

    int info = 0;
    int warn = 0;
    int error = 0;
    int invalid = 0;
    std::string line;
    while (std::getline(input, line)) {
        const auto separator = line.find('|');
        if (separator == std::string::npos) {
            ++invalid;
            continue;
        }
        const std::string level = line.substr(0, separator);
        if (level == "INFO") ++info;
        else if (level == "WARN") ++warn;
        else if (level == "ERROR") ++error;
        else ++invalid;
    }
    if (!input.eof() && input.fail()) {
        std::cout << "READ_ERROR\n";
        return 0;
    }
    std::cout << "INFO " << info << "\nWARN " << warn
              << "\nERROR " << error << "\nINVALID " << invalid << '\n';
}
