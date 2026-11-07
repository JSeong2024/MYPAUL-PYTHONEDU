#include <print>
#include <utility>

class Handle {
public:
    explicit Handle(int id) noexcept : id_(id) {}
    Handle(const Handle&) = delete;
    Handle& operator=(const Handle&) = delete;
    Handle(Handle&& other) noexcept : id_(std::exchange(other.id_, -1)) {}
    Handle& operator=(Handle&& other) noexcept {
        if (this != &other) id_ = std::exchange(other.id_, -1);
        return *this;
    }
    [[nodiscard]] int id() const noexcept { return id_; }
private:
    int id_{-1};
};

int main() {
    Handle first{42};
    Handle second{std::move(first)};
    std::println("New: {}, Old: {}", second.id(), first.id());
}
