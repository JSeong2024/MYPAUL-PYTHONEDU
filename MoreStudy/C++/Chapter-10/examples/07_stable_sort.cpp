#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Task {
    std::string name;
    int priority{};
};

int main() {
    std::vector<Task> tasks{{"scan", 2}, {"save", 1}, {"upload", 2}};
    std::stable_sort(tasks.begin(), tasks.end(), [](const Task& a, const Task& b) {
        return a.priority > b.priority;
    });

    for (const auto& task : tasks) {
        std::cout << task.name << ": " << task.priority << '\n';
    }
}
