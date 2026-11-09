#include <iostream>
int main() {
#ifdef SENSOR_TRACE
    std::cout << "Trace: enabled\n";
#else
    std::cout << "Trace: disabled\n";
#endif
}
