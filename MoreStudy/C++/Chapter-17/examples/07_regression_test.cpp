#include <iostream>
#include <stdexcept>
#include <vector>
int last_or_zero(const std::vector<int>& data) {
    return data.empty() ? 0 : data.back();
}
int main() {
    if(last_or_zero({})!=0 || last_or_zero({4,7})!=7) throw std::runtime_error("regression");
    std::cout << "Regression: PASS\n";
}
