#include "inventory.hpp"

namespace inventory {

std::optional<int> remaining_stock(int received, int shipped) noexcept {
    if (received < 0 || shipped < 0 || shipped > received) {
        return std::nullopt;
    }
    return received - shipped;
}

}  // namespace inventory
