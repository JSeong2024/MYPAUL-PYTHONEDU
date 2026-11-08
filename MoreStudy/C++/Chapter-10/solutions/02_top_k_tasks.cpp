#include <iostream>
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

[[nodiscard]] std::vector<Task> top_k(const std::vector<Task>& tasks, int k) {
    std::priority_queue<Task, std::vector<Task>, LowerPriority> queue;
    for (const auto& task : tasks) {
        queue.push(task);
    }
    std::vector<Task> result;
    for (int i = 0; i < k && !queue.empty(); ++i) {
        result.push_back(queue.top());
        queue.pop();
    }
    return result;
}

int main() {
    int n{}, k{};
    if (!(std::cin >> n >> k) || n < 1 || n > 10'000 || k < 1 || k > n) {
        std::cerr << "Error: invalid task count\n";
        return 1;
    }
    std::vector<Task> tasks;
    tasks.reserve(static_cast<std::size_t>(n));
    for (int i = 0; i < n; ++i) {
        Task task;
        if (!(std::cin >> task.name >> task.priority) ||
            task.priority < 0 || task.priority > 100) {
            std::cerr << "Error: invalid task\n";
            return 1;
        }
        tasks.push_back(task);
    }
    for (const auto& task : top_k(tasks, k)) {
        std::cout << task.name << ' ' << task.priority << '\n';
    }
}
