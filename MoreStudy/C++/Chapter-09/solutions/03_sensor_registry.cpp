#include <algorithm>
#include <memory>
#include <print>
#include <ranges>
#include <string>
#include <string_view>
#include <utility>
#include <vector>

struct ISensor {
    virtual ~ISensor() = default;
    [[nodiscard]] virtual std::string_view id() const noexcept = 0;
};

class FixedSensor final : public ISensor {
public:
    explicit FixedSensor(std::string id) : id_(std::move(id)) {}
    [[nodiscard]] std::string_view id() const noexcept override { return id_; }

private:
    std::string id_;
};

class Registry {
public:
    [[nodiscard]] bool add(std::unique_ptr<ISensor> sensor) {
        if (!sensor || sensor->id().empty()) return false;
        if (std::ranges::any_of(sensors_, [&](const auto& saved) {
                return saved->id() == sensor->id();
            })) return false;
        sensors_.push_back(std::move(sensor));
        return true;
    }
    [[nodiscard]] std::size_t size() const noexcept { return sensors_.size(); }

private:
    std::vector<std::unique_ptr<ISensor>> sensors_;
};

int main() {
    Registry registry;
    const bool first = registry.add(std::make_unique<FixedSensor>("S-01"));
    const bool duplicate = registry.add(std::make_unique<FixedSensor>("S-01"));
    const bool empty = registry.add(std::make_unique<FixedSensor>(""));
    const bool null_added = registry.add(nullptr);
    std::println("First: {}, duplicate: {}, empty: {}, null: {}, count: {}",
                 first, duplicate, empty, null_added, registry.size());
}
