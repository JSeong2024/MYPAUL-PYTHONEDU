#include <iostream>
#include <mutex>
#include <stdexcept>
#include <thread>
#include <vector>

class StockLedger {
public:
    explicit StockLedger(int initial) : remaining_(initial) {
        if (initial < 0) throw std::invalid_argument("negative stock");
    }
    [[nodiscard]] bool purchase(int quantity) {
        std::lock_guard lock{mutex_};
        if (quantity <= 0 || quantity > remaining_) return false;
        remaining_ -= quantity;
        sold_ += quantity;
        return true;
    }
    [[nodiscard]] int remaining() const {
        std::lock_guard lock{mutex_};
        return remaining_;
    }
    [[nodiscard]] int sold_units() const {
        std::lock_guard lock{mutex_};
        return sold_;
    }
private:
    mutable std::mutex mutex_;
    int remaining_{};
    int sold_{};
};

#ifndef CH14_LIBRARY_ONLY
int main() {
    StockLedger ledger{150};
    std::vector<std::jthread> buyers;
    for (int i = 0; i < 4; ++i) {
        buyers.emplace_back([&] {
            for (int j = 0; j < 100; ++j) (void)ledger.purchase(1);
        });
    }
    for (auto& buyer : buyers) buyer.join();
    std::cout << "Sold: " << ledger.sold_units()
              << ", Remaining: " << ledger.remaining() << '\n';
}
#endif
