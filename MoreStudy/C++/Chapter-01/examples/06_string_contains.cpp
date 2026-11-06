#include <print>
#include <string>

int main() {
    using std::println;

    const std::string filename{"monthly_report.csv"};
    if (filename.contains("report")) {
        println("Report file: {}", filename);
    }

    return 0;
}
