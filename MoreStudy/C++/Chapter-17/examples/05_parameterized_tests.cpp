#include <array>
#include <iostream>
#include <stdexcept>
int shipping(int weight) {
    if (weight <= 0) throw std::invalid_argument("weight");
    return 2000 + (weight-1)/500 * 500;
}
int main() {
    struct Case {int weight; int price;};
    constexpr std::array samples{Case{1,2000},Case{500,2000},Case{501,2500},Case{1000,2500}};
    for (auto c: samples) if(shipping(c.weight)!=c.price) throw std::runtime_error("case");
    std::cout << "Shipping cases: 4\n";
}
