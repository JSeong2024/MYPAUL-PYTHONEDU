#include <map>
#include <print>
#include <set>
#include <string>

int main() {
    std::map<std::string, int> inventory{{"battery", 4}, {"camera", 2}};
    inventory.insert_or_assign("battery", 5);
    std::set<int> channel_ids{8, 3, 8, 5};

    for (const auto& [name, quantity] : inventory) {
        std::println("{}: {}", name, quantity);
    }
    std::println("Unique channels: {}", channel_ids.size());
    if (const auto it = channel_ids.lower_bound(4); it != channel_ids.end()) {
        std::println("First channel >= 4: {}", *it);
    }
}
