#include <algorithm>
#include <cstddef>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <utility>

class IntBuffer {
public:
    explicit IntBuffer(std::size_t size)
        : data_(size ? std::make_unique<int[]>(size) : nullptr), size_(size) {}
    ~IntBuffer() = default;

    IntBuffer(const IntBuffer& other) : IntBuffer(other.size_) {
        if (size_ != 0) {
            std::copy_n(other.data_.get(), size_, data_.get());
        }
    }
    IntBuffer& operator=(const IntBuffer& other) {
        if (this != &other) {
            IntBuffer copy{other};
            swap(copy);
        }
        return *this;
    }
    IntBuffer(IntBuffer&& other) noexcept
        : data_(std::move(other.data_)), size_(std::exchange(other.size_, 0)) {}
    IntBuffer& operator=(IntBuffer&& other) noexcept {
        if (this != &other) {
            data_ = std::move(other.data_);
            size_ = std::exchange(other.size_, 0);
        }
        return *this;
    }
    void swap(IntBuffer& other) noexcept {
        data_.swap(other.data_);
        std::swap(size_, other.size_);
    }
    [[nodiscard]] std::size_t size() const noexcept { return size_; }
    [[nodiscard]] int& at(std::size_t index) {
        if (index >= size_) throw std::out_of_range("invalid index");
        return data_[index];
    }
private:
    std::unique_ptr<int[]> data_;
    std::size_t size_{};
};

int main() {
    IntBuffer first{2};
    first.at(0) = 7;
    first.at(1) = 9;
    IntBuffer copied{first};
    copied.at(0) = 50;
    IntBuffer moved{std::move(first)};
    std::cout << "Copy: " << copied.at(0) << ", Moved: " << moved.at(0)
              << ", Old size: " << first.size() << '\n';
}
