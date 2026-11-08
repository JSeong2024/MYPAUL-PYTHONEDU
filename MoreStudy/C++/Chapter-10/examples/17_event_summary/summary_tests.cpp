#include "summary.hpp"

#include <iostream>

int main() {
    events::Summary report;
    if (events::distinct_count(report) != 0 || report.total != 0) return 1;
    if (events::add_event(report, "")) return 2;
    if (!events::add_event(report, "WARN")) return 3;
    if (!events::add_event(report, "WARN")) return 4;
    if (!events::add_event(report, "INFO")) return 5;
    if (report.total != 3 || events::distinct_count(report) != 2) return 6;
    if (report.frequency.at("WARN") != 2) return 7;
    std::cout << "Summary tests: PASS\n";
}
