#include <print>
#include <queue>
#include <string_view>
#include <vector>

struct Job {
    std::string_view id;
    int priority;
};

struct LowerPriority {
    bool operator()(const Job& a, const Job& b) const {
        if (a.priority != b.priority) {
            return a.priority < b.priority;
        }
        return a.id > b.id;  // 동점에서는 사전순으로 앞선 ID 우선
    }
};

int main() {
    std::priority_queue<Job, std::vector<Job>, LowerPriority> queue;
    queue.push({"save", 20});
    queue.push({"scan", 90});
    queue.push({"report", 90});
    while (!queue.empty()) {
        std::println("{}: {}", queue.top().id, queue.top().priority);
        queue.pop();
    }
}
