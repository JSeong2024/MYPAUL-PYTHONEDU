#include <cstddef>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

class JobQueue {
public:
    void add(std::string job) {
        jobs_.push_back(std::move(job));
    }

    [[nodiscard]] std::size_t size() const noexcept { return jobs_.size(); }

private:
    std::vector<std::string> jobs_;
};

int main() {
    JobQueue original;
    original.add("Scan");
    JobQueue copied = original;
    JobQueue moved = std::move(original);
    std::cout << "Copied: " << copied.size()
              << ", moved: " << moved.size() << '\n';
}
