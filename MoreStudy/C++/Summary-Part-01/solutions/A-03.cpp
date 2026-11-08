#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Task {
    std::string id;
    int priority = 0;
};

int main() {
    int count = 0;
    if (!(std::cin >> count) || count < 1 || count > 1000) {
        std::cout << "INVALID\n";
        return 0;
    }
    std::vector<Task> tasks;
    for (int i = 0; i < count; ++i) {
        Task task;
        if (!(std::cin >> task.id >> task.priority) ||
            task.priority < 0 || task.priority > 10) {
            std::cout << "INVALID\n";
            return 0;
        }
        tasks.push_back(task);
    }
    std::stable_sort(tasks.begin(), tasks.end(), [](const Task& a, const Task& b) {
        return a.priority > b.priority;
    });
    for (const auto& task : tasks) std::cout << task.id << '\n';
}
