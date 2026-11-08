#include <iostream>
#include <queue>
#include <stack>

int main() {
    std::queue<int> pending;
    pending.push(101);
    pending.push(102);
    std::cout << "Next queue item: " << pending.front() << '\n';
    pending.pop();

    std::stack<int> history;
    history.push(1);
    history.push(2);
    std::cout << "Latest history item: " << history.top() << '\n';
    history.pop();

    std::priority_queue<int> priorities;
    priorities.push(20);
    priorities.push(90);
    priorities.push(40);
    std::cout << "Highest priority: " << priorities.top() << '\n';
}
