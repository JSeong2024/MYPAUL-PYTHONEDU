#include <print>
#include <queue>
#include <stack>

int main() {
    std::queue<int> pending;
    pending.push(101);
    pending.push(102);
    std::println("Next queue item: {}", pending.front());
    pending.pop();

    std::stack<int> history;
    history.push(1);
    history.push(2);
    std::println("Latest history item: {}", history.top());
    history.pop();

    std::priority_queue<int> priorities;
    priorities.push(20);
    priorities.push(90);
    priorities.push(40);
    std::println("Highest priority: {}", priorities.top());
}
