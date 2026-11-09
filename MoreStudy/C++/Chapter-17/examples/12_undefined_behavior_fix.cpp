#include <iostream>
#include <limits>
#include <optional>
std::optional<int> checked_add(int a,int b) {
    if ((b>0 && a>std::numeric_limits<int>::max()-b) ||
        (b<0 && a<std::numeric_limits<int>::min()-b)) return std::nullopt;
    return a+b;
}
int main() {
    const auto safe=checked_add(10,20);
    const auto invalid=checked_add(std::numeric_limits<int>::max(),1);
    if(!safe || *safe!=30 || invalid) return 1;
    std::cout << "Overflow: rejected\n";
}
