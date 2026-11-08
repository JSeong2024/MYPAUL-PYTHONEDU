#include <cstdint>
#include <iostream>
#include <limits>

class BankAccount {
public:
    explicit BankAccount(std::int64_t opening_cents) noexcept
        : balance_cents_{opening_cents >= 0 ? opening_cents : 0} {}

    [[nodiscard]] bool deposit(std::int64_t cents) noexcept {
        // TODO: 양수 입금만 허용하고, int64_t 오버플로를 검사하세요.
        (void)cents;
        return false;
    }

    [[nodiscard]] bool withdraw(std::int64_t cents) noexcept {
        // TODO: 양수 출금만 허용하고, 잔액보다 큰 출금을 거절하세요.
        (void)cents;
        return false;
    }

    [[nodiscard]] std::int64_t balance_cents() const noexcept {
        return balance_cents_;
    }

private:
    std::int64_t balance_cents_{};
};

int main() {
    BankAccount account{10'000};
    const bool deposited{account.deposit(2'500)};
    const bool withdrawn{account.withdraw(4'000)};
    std::cout << std::boolalpha << "Deposit: " << deposited
              << ", withdraw: " << withdrawn
              << ", balance: " << account.balance_cents() << " cents\n";
}
