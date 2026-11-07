#include <memory>
#include <print>
#include <utility>
#include <vector>

struct Job {
    explicit Job(int value) : id(std::make_unique<int>(value)) {}
    std::unique_ptr<int> id;
};

int main() {
    std::vector<Job> jobs;
    jobs.emplace_back(10);
    Job task{20};
    jobs.push_back(std::move(task));
    std::println("Jobs: {} / {}", *jobs[0].id, *jobs[1].id);
}
