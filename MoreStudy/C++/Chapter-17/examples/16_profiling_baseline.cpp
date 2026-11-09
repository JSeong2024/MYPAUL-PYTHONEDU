#include <algorithm>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
int main() {
    std::vector<std::string> ids{"D3","D1","D2","D1"};
    std::sort(ids.begin(),ids.end());
    const auto matches=std::count(ids.begin(),ids.end(),"D1");
    if(matches!=2)throw std::runtime_error("baseline");
    std::cout << "Matches: " << matches << '\n';
}
