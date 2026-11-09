#include <array>
#include <iostream>
#include <memory>
#include <vector>

int main() {
    const std::array<int, 3> fixed{2, 4, 6};
    const std::vector<int> dynamic{3, 6, 9};
    auto owned = std::make_unique<int>(12);
    std::cout << "Fixed: " << fixed[0] << ", Dynamic: " << dynamic[1]
              << ", Owned: " << *owned << "\n";
}
