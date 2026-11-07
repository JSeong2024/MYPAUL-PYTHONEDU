#include <cstdio>
#include <iostream>
#include <print>
#include <queue>
#include <string>
#include <vector>

struct Task {
    std::string name;
    int priority{};
};
struct LowerPriority {
    bool operator()(const Task& a, const Task& b) const {
        if (a.priority != b.priority) return a.priority < b.priority;
        return a.name > b.name;
    }
};

int main() {
    int n{}, k{};
    if (!(std::cin >> n >> k) || n < 1 || n > 10'000 || k < 1 || k > n) {
        std::println(stderr, "Invalid size");
        return 1;
    }
    std::priority_queue<Task, std::vector<Task>, LowerPriority> tasks;
    for (int i = 0; i < n; ++i) {
        Task task;
        if (!(std::cin >> task.name >> task.priority) ||
            task.priority < 0 || task.priority > 100) {
            std::println(stderr, "Invalid task");
            return 1;
        }
        tasks.push(std::move(task));
    }
    for (int i = 0; i < k; ++i) {
        const auto& task = tasks.top();
        std::println("{} {}", task.name, task.priority);
        tasks.pop();
    }
}
