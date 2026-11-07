#include <memory>
#include <print>
#include <string>
#include <utility>

struct Camera {
    explicit Camera(std::string id) : id(std::move(id)) {}
    std::string id;
};

int main() {
    auto source = std::make_unique<Camera>("cam-01");
    auto destination = std::move(source);
    std::println("Source exists: {}", source != nullptr);
    if (destination) std::println("Camera: {}", destination->id);
}
