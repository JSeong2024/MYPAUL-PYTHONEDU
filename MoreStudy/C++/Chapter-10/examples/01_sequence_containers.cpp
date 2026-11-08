#include <deque>
#include <iostream>
#include <iterator>
#include <list>
#include <vector>

int main() {
    std::vector<int> samples{20, 22, 19};
    samples.push_back(21);

    std::deque<int> pending{2, 3};
    pending.push_front(1);

    std::list<int> checkpoints{10, 30};
    checkpoints.insert(std::next(checkpoints.begin()), 20);

    std::cout << "Samples: " << samples.size() << '\n';
    std::cout << "First task: " << pending.front() << '\n';
    for (const int point : checkpoints) {
        std::cout << "Checkpoint: " << point << '\n';
    }
}
