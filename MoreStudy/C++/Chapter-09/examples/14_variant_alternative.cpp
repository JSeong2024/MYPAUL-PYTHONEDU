#include <iostream>
#include <variant>

struct Temperature { int celsius{}; };
struct Distance { int centimeters{}; };

int main() {
    const std::variant<Temperature, Distance> reading{Distance{35}};
    if (const auto* distance = std::get_if<Distance>(&reading)) {
        std::cout << "Distance: " << distance->centimeters << " cm\n";
    } else if (const auto* temperature = std::get_if<Temperature>(&reading)) {
        std::cout << "Temperature: " << temperature->celsius << " C\n";
    }
}
