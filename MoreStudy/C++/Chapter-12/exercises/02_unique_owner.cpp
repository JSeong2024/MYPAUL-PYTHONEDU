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
    // TODO: destination으로 Ownership을 이전하고
    // source가 nullptr인지 검증한 뒤 Camera ID를 출력
    std::println("Source exists: {}", source != nullptr);
}
