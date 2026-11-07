#include <memory>
#include <print>
#include <vector>

class ICommand {
public:
    virtual ~ICommand() = default;
    virtual void execute() const = 0;
};

class StopMotor final : public ICommand {
public:
    void execute() const override { std::println("Motor: stop"); }
};

class TurnOnLight final : public ICommand {
public:
    void execute() const override { std::println("Light: on"); }
};

int main() {
    std::vector<std::unique_ptr<ICommand>> commands;
    commands.push_back(std::make_unique<StopMotor>());
    commands.push_back(std::make_unique<TurnOnLight>());

    for (const auto& command : commands) {
        command->execute();
    }
}
