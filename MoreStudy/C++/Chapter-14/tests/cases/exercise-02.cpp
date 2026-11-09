#include <iostream>
#include <stdexcept>
#include <thread>
#include <vector>
#include CH14_SOURCE_PATH

void require(bool condition) { if (!condition) throw std::runtime_error("stock ledger"); }
int main() {
    StockLedger ledger{150};
    require(!ledger.purchase(0));
    require(!ledger.purchase(-1));
    std::vector<std::jthread> buyers;
    for (int i=0;i<8;++i) buyers.emplace_back([&] {
        for (int j=0;j<100;++j) (void)ledger.purchase(1);
    });
    for (auto& buyer: buyers) buyer.join();
    require(ledger.remaining()==0 && ledger.sold_units()==150);
    require(!ledger.purchase(1));
    bool invalid=false;
    try { StockLedger bad{-1}; }
    catch (const std::invalid_argument&) { invalid=true; }
    require(invalid);
    StockLedger other{20};
    require(other.purchase(6));
    require(other.remaining()==14 && other.sold_units()==6);
    std::cout << "PASS\n";
}
