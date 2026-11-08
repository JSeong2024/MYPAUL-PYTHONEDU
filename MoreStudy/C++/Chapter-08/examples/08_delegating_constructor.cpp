#include <iostream>
#include <string>
#include <utility>

class Sensor {
public:
    explicit Sensor(std::string name) : Sensor{std::move(name), 100} {}

    Sensor(std::string name, int threshold)
        : name_{std::move(name)}, threshold_{threshold} {}

    void print() const {
        std::cout << name_ << ": threshold " << threshold_ << '\n';
    }

private:
    std::string name_;
    int threshold_{};
};

int main() {
    const Sensor first{"Temperature"};
    const Sensor second{"Vibration", 80};
    first.print();
    second.print();
}
