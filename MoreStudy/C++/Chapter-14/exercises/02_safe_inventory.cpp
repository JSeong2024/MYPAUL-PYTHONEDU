#include <iostream>
#include <mutex>
#include <stdexcept>
#include <thread>
#include <vector>

class StockLedger {
public:
    explicit StockLedger(int initial) : remaining_(initial) {
        // TODO: 잘못된 초기 재고를 검사합니다.
    }
    [[nodiscard]] bool purchase(int quantity) {
        // TODO: 수량 검증·판매 확정·재고 변경을 하나의 임계 구역으로 처리합니다.
        (void)quantity;
        return false;
    }
    [[nodiscard]] int remaining() const { return remaining_; }
    [[nodiscard]] int sold_units() const { return sold_; }
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
