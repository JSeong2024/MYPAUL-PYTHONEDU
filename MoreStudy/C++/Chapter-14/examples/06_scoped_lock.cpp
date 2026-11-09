#include <iostream>
#include <mutex>
#include <thread>
#include <vector>

struct Accounts {
    std::mutex left_mutex;
    std::mutex right_mutex;
    int left{100};
    int right{50};
    void transfer(int amount) {
        std::scoped_lock lock{left_mutex, right_mutex};
        if (amount >= 0 && left >= amount) {
            left -= amount;
            right += amount;
        }
    }
};

int main() {
    Accounts accounts;
    std::vector<std::jthread> workers;
    for (int i = 0; i < 5; ++i) workers.emplace_back([&] { accounts.transfer(10); });
    for (auto& worker : workers) worker.join();
    std::cout << "Balances: " << accounts.left << ", " << accounts.right << '\n';
}
