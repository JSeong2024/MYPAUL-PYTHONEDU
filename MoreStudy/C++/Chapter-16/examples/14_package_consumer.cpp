#include <algorithm>
#include <iostream>
#include <vector>
int main() {
    std::vector<int> values{6, 2, 4};
    std::ranges::sort(values);
    std::cout << "First: " << values.front() << '\n';
}
