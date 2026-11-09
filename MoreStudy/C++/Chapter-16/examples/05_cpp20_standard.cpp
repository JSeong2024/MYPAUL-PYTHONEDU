#include <iostream>
#include <map>
#include <string>
int main() {
    const std::map<std::string, int> devices{{"A", 12}, {"B", 21}};
    std::cout << "Has B: " << std::boolalpha << devices.contains("B") << '\n';
}
