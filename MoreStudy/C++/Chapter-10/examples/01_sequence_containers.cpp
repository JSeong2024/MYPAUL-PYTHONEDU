#include <iterator>
#include <deque>
#include <list>
#include <print>
#include <vector>

int main() {
    std::vector<int> samples{20, 22, 19};
    samples.push_back(21);
    std::deque<int> pending{2, 3};
    pending.push_front(1);
    std::list<int> checkpoints{10, 30};
    checkpoints.insert(std::next(checkpoints.begin()), 20);

    std::println("Samples: {}", samples.size());
    std::println("First task: {}", pending.front());
    for (const int point : checkpoints) {
        std::println("Checkpoint: {}", point);
    }
}
