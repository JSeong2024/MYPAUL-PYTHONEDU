#include <iostream>
#include <memory>
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
    std::cout << "Jobs: " << *jobs.at(0).id << " / " << *jobs.at(1).id << '\n';
}
