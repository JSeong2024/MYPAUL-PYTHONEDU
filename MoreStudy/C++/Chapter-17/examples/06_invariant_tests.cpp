#include <algorithm>
#include <array>
#include <iostream>
#include <numeric>
#include <stdexcept>
int main() {
    std::array values{9,2,5,2,7};
    const auto sum=std::accumulate(values.begin(),values.end(),0);
    std::sort(values.begin(),values.end());
    if(sum!=std::accumulate(values.begin(),values.end(),0) ||
       !std::is_sorted(values.begin(),values.end())) throw std::runtime_error("invariant");
    std::cout << "Invariant: preserved\n";
}
