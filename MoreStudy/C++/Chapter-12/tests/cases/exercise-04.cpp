#include <cassert>
#include <string>
#include CH12_SOURCE_PATH
int main() {
    auto valid = make_device("sensor-A", 0);
    assert(valid && valid->name == "sensor-A" && valid->limit == 0);
    assert(make_device("X9", 100));
    assert(!make_device("", 50));
    assert(!make_device("invalid name", 50));
    assert(!make_device("sensor_", 50));
    assert(!make_device(std::string(17, 'A'), 50));
    assert(make_device(std::string(16, 'A'), 50));
    assert(!make_device("valid", -1));
    assert(!make_device("valid", 101));
}
