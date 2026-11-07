#include "13_device_registry.hpp"

#include <algorithm>
#include <utility>

bool DeviceRegistry::add(std::string id) {
    if (id.empty() || contains(id)) {
        return false;
    }
    ids_.push_back(std::move(id));
    return true;
}

bool DeviceRegistry::contains(std::string_view id) const {
    return std::ranges::any_of(ids_, [id](const std::string& current) {
        return current == id;
    });
}

std::size_t DeviceRegistry::size() const noexcept {
    return ids_.size();
}
