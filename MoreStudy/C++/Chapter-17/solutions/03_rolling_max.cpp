#include <algorithm>
#include <cstddef>
#include <span>
#include <stdexcept>
#include <vector>
std::vector<int> rolling_max(std::span<const int> values, std::size_t window) {
    if(window==0 || window>values.size()) throw std::invalid_argument("invalid window");
    std::vector<int> result;
    result.reserve(values.size()-window+1);
    for(std::size_t i=0; i<=values.size()-window;++i) {
        result.push_back(*std::max_element(values.begin()+static_cast<std::ptrdiff_t>(i),
                                           values.begin()+static_cast<std::ptrdiff_t>(i+window)));
    }
    return result;
}
#ifndef CH17_LIBRARY_ONLY
#include <iostream>
#include <vector>
int main(){std::vector v{2,8,3,5};for(int n:rolling_max(v,2))std::cout<<n<<' ';std::cout<<'\n';}
#endif
