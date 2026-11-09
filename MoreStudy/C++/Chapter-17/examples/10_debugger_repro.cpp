#include <array>
#include <iostream>
#include <stdexcept>
int sum_positive(const std::array<int,4>& values) {
    int total=0;
    for(int value:values) if(value>0) total+=value;
    return total;
}
int main() {
    const std::array readings{-3,5,0,7};
    const int total=sum_positive(readings);
    if(total!=12) throw std::runtime_error("sum mismatch");
    std::cout << "Positive sum: " << total << '\n';
}
