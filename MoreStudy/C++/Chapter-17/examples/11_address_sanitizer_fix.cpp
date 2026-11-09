#include <iostream>
#include <stdexcept>
#include <vector>
int checked_element(const std::vector<int>& values,std::size_t index) {
    return values.at(index);
}
int main() {
    const std::vector readings{10,20,30};
    bool caught=false;
    try { (void)checked_element(readings,3); }
    catch(const std::out_of_range&) { caught=true; }
    if (!caught) throw std::runtime_error("missing bounds check");
    std::cout << "Bounds: handled\n";
}
