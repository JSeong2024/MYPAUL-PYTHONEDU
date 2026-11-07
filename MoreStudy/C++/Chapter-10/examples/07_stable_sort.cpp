#include <algorithm>
#include <print>
#include <string_view>
#include <vector>

struct Task {
    std::string_view name;
    int priority;
};

int main() {
    std::vector<Task> tasks{{"scan", 5}, {"save", 8}, {"report", 5}};
    std::ranges::stable_sort(tasks, [](const Task& a, const Task& b) {
        return a.priority > b.priority;
    });
    for (const auto& task : tasks) {
        std::println("{}: {}", task.name, task.priority);
    }
}
