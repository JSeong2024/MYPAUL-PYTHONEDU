#include <memory>
#include <print>
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
        // TODO: nullptr, 빈 ID, 중복 ID는 거부합니다.
        // 성공하면 vector에 std::move(sensor)로 소유권을 이전합니다.
        (void)sensor;
        return false;
    }
    [[nodiscard]] std::size_t size() const noexcept { return sensors_.size(); }

private:
    std::vector<std::unique_ptr<ISensor>> sensors_;
};

int main() {
    Registry registry;
    const bool added = registry.add(std::make_unique<FixedSensor>("S-01"));
    std::println("Added: {}, count: {}", added, registry.size());
}
