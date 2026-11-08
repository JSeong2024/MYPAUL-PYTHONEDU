#include <iomanip>
#include <iostream>
#include <map>
#include <string>

struct DeviceStats {
    long long total_latency{};
    int events{};
};

struct Report {
    std::map<std::string, DeviceStats> devices;
    long long all_latency{};
    int total{};
    int warnings{};
    int errors{};
};

void add_record(Report& report, const std::string& device,
                const std::string& level, int latency) {
    // TODO: 장치별 건수와 지연 시간 합계, 전체 건수, WARN/ERROR 건수를 갱신합니다.
    (void)report;
    (void)device;
    (void)level;
    (void)latency;
}

int main() {
    int n{};
    std::cout << "Records (1-100): " << std::flush;
    if (!(std::cin >> n) || n < 1 || n > 100) {
        std::cerr << "Error: invalid record count\n";
        return 1;
    }
    Report report;
    for (int i = 0; i < n; ++i) {
        std::string device, level;
        int latency{};
        std::cout << "Record " << i + 1 << " (device level latency_ms): " << std::flush;
        if (!(std::cin >> device >> level >> latency)) {
            std::cerr << "Error: invalid record\n";
            return 1;
        }
        if (device.size() > 20 ||
            (level != "INFO" && level != "WARN" && level != "ERROR") ||
            latency < 0 || latency > 1'000'000) {
            std::cerr << "Error: invalid record\n";
            return 1;
        }
        add_record(report, device, level, latency);
    }

    std::cout << std::fixed << std::setprecision(2);
    std::cout << "--- Device Event Summary ---\n";
    std::cout << "Events: " << report.total << '\n';
    std::cout << "Devices: " << report.devices.size() << '\n';
    std::cout << "Warnings: " << report.warnings << '\n';
    std::cout << "Errors: " << report.errors << '\n';
    std::cout << "Average latency: "
              << static_cast<double>(report.all_latency) / report.total << " ms\n";

    std::cout << std::setprecision(1);
    std::string top_device;
    int most_events{};
    for (const auto& [device, stats] : report.devices) {
        std::cout << device << ": " << stats.events << " events, avg "
                  << static_cast<double>(stats.total_latency) / stats.events << " ms\n";
        if (stats.events > most_events) {
            most_events = stats.events;
            top_device = device;
        }
    }
    std::cout << "Top device: " << top_device << " (" << most_events << ")\n";
}
