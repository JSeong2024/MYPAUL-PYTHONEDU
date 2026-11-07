#pragma once

#include <memory>
#include <optional>
#include <string>
#include <string_view>
#include <vector>

struct Sample {
    std::string id;
    std::optional<double> value;
    std::string unit;
};

class ISensor {
public:
    virtual ~ISensor() = default;
    [[nodiscard]] virtual std::string_view id() const noexcept = 0;
    [[nodiscard]] virtual std::string_view unit() const noexcept = 0;
    [[nodiscard]] virtual std::optional<double> read() const noexcept = 0;
};

class TemperatureSensor final : public ISensor {
public:
    TemperatureSensor(std::string id, double celsius);
    [[nodiscard]] std::string_view id() const noexcept override;
    [[nodiscard]] std::string_view unit() const noexcept override;
    [[nodiscard]] std::optional<double> read() const noexcept override;

private:
    std::string id_;
    double celsius_{};
};

class BatterySensor final : public ISensor {
public:
    BatterySensor(std::string id, double percent);
    [[nodiscard]] std::string_view id() const noexcept override;
    [[nodiscard]] std::string_view unit() const noexcept override;
    [[nodiscard]] std::optional<double> read() const noexcept override;

private:
    std::string id_;
    double percent_{};
};

class Monitor {
public:
    [[nodiscard]] bool add(std::unique_ptr<ISensor> sensor);
    [[nodiscard]] std::vector<Sample> collect() const;

private:
    std::vector<std::unique_ptr<ISensor>> sensors_;
};
