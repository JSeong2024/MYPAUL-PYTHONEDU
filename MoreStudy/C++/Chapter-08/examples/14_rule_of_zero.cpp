#include <print>
#include <string>
#include <utility>
#include <vector>

class JobQueue {
public:
    void add(std::string job) {
        jobs_.push_back(std::move(job));
    }

    [[nodiscard]] std::size_t size() const noexcept {
        return jobs_.size();
    }

private:
    std::vector<std::string> jobs_;
};

int main() {
    JobQueue original;
    original.add("Scan");

    JobQueue copied = original;
    JobQueue moved = std::move(original);

    std::println("Copied: {}, moved: {}", copied.size(), moved.size());
    // 이동 후 original은 유효하지만 내부 요소 개수를 가정하지 않음.
}
