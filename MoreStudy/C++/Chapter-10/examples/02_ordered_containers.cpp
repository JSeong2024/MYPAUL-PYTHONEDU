#include <iostream>
#include <map>
#include <set>
#include <string>

int main() {
    std::map<std::string, int> inventory{{"battery", 4}, {"camera", 2}};
    inventory.insert_or_assign("battery", 5);
    std::set<int> channel_ids{8, 3, 8, 5};

    for (const auto& [name, quantity] : inventory) {
        std::cout << name << ": " << quantity << '\n';
    }
    std::cout << "Unique channels: " << channel_ids.size() << '\n';
    if (const auto it = channel_ids.lower_bound(4); it != channel_ids.end()) {
        std::cout << "First channel >= 4: " << *it << '\n';
    }
}
