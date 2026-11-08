#pragma once
#include <memory>
#include <string_view>
#include <vector>

namespace monitor {
class Sensor {
public:
    virtual ~Sensor() = default;
    [[nodiscard]] virtual std::string_view kind() const noexcept = 0;
    [[nodiscard]] virtual int reading() const noexcept = 0;
    [[nodiscard]] virtual bool alert() const noexcept = 0;
};
class TemperatureSensor final : public Sensor {
public:
    explicit TemperatureSensor(int value) : value_{value} {}
    [[nodiscard]] std::string_view kind() const noexcept override;
    [[nodiscard]] int reading() const noexcept override;
    [[nodiscard]] bool alert() const noexcept override;
private:
    int value_{};
};
class DistanceSensor final : public Sensor {
public:
    explicit DistanceSensor(int value) : value_{value} {}
    [[nodiscard]] std::string_view kind() const noexcept override;
    [[nodiscard]] int reading() const noexcept override;
    [[nodiscard]] bool alert() const noexcept override;
private:
    int value_{};
};
struct Report { int total{}; int alerts{}; };
[[nodiscard]] Report evaluate(const std::vector<std::unique_ptr<Sensor>>& sensors);
} // namespace monitor
