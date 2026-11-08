#include <iostream>
#include <utility>

// 실제 장치 대신, 정리 횟수를 세는 가상의 자원 식별자를 사용합니다.
class OwnedHandle {
public:
    explicit OwnedHandle(int id) noexcept : id_(id) {}
    ~OwnedHandle() { release(); }
    OwnedHandle(const OwnedHandle&) = delete;
    OwnedHandle& operator=(const OwnedHandle&) = delete;
    OwnedHandle(OwnedHandle&& other) noexcept
        : id_(std::exchange(other.id_, -1)) {}
    OwnedHandle& operator=(OwnedHandle&& other) noexcept {
        if (this != &other) {
            release();
            id_ = std::exchange(other.id_, -1);
        }
        return *this;
    }
    [[nodiscard]] int id() const noexcept { return id_; }
    [[nodiscard]] static int released() noexcept { return released_; }
private:
    void release() noexcept {
        if (id_ != -1) {
            ++released_;
            id_ = -1;
        }
    }
    int id_{-1};
    inline static int released_{0};
};

int main() {
    {
        OwnedHandle first{42};
        OwnedHandle second{std::move(first)};
        std::cout << "New: " << second.id() << ", Old: " << first.id() << '\n';
    }
    std::cout << "Released: " << OwnedHandle::released() << '\n';
}
