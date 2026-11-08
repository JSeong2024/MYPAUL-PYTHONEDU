#include "summary.hpp"

#include <iostream>

int main() {
    events::Summary report;
    for (const char* name : {"WARN", "INFO", "WARN", "ERROR", "INFO"}) {
        if (!events::add_event(report, name)) {
            return 1;
        }
    }
    std::cout << "Total: " << report.total << '\n';
    std::cout << "Distinct: " << events::distinct_count(report) << '\n';
    for (const auto& [name, count] : report.frequency) {
        std::cout << name << ": " << count << '\n';
    }
}
