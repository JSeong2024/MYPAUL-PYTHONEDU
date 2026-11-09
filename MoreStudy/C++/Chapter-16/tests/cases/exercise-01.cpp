#include <stdexcept>
#include <string>
int main() {
    if (versioned_name("sensor", 3) != "sensor-v3") return 1;
    try { (void)versioned_name("", 1); return 2; }
    catch (const std::invalid_argument&) {}
    try { (void)versioned_name("a", 0); return 3; }
    catch (const std::invalid_argument&) {}
    return 0;
}
