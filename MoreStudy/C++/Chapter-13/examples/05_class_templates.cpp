#include <cstddef>
#include <iostream>
#include <stdexcept>
#include <vector>

template <typename T>
class SampleBuffer {
public:
    void add(const T& item) { samples_.push_back(item); }
    [[nodiscard]] const T& at(std::size_t index) const { return samples_.at(index); }
    [[nodiscard]] std::size_t size() const noexcept { return samples_.size(); }
private:
    std::vector<T> samples_;
};

int main() {
    SampleBuffer<int> integers;
    integers.add(12);
    integers.add(19);
    SampleBuffer<double> decimals;
    decimals.add(2.5);
    std::cout << "Integer samples: " << integers.size() << '\n';
    std::cout << "First double: " << decimals.at(0) << '\n';
}
