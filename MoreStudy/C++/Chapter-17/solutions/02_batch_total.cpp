#include <span>
#include <stdexcept>
int batch_total(std::span<const int> readings) {
    int sum=0;
    for(int value: readings) {
        if(value<0 || value>100)throw std::invalid_argument("reading out of range");
        sum+=value;  // 최대 10,000개 * 100 = 1,000,000
    }
    return sum;
}
#ifndef CH17_LIBRARY_ONLY
#include <iostream>
#include <vector>
int main(){std::vector v{10,20,30};std::cout << "Total: " << batch_total(v) << '\n';}
#endif
