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
        if (a.priority != b.priority) {
            return a.priority < b.priority;
        }
        return a.name > b.name;  // 동점이면 이름 오름차순
    }
};

int main() {
    std::priority_queue<Task, std::vector<Task>, LowerPriority> tasks;
    tasks.push({"scan", 70});
    tasks.push({"upload", 90});
    tasks.push({"navigate", 90});

    while (!tasks.empty()) {
        const Task& next = tasks.top();
        std::cout << next.name << ": " << next.priority << '\n';
        tasks.pop();
    }
}
