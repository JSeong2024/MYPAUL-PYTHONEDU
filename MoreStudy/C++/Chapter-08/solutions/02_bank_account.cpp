#include <cstdint>
#include <iostream>
#include <limits>

class BankAccount {
public:
    explicit BankAccount(std::int64_t opening_cents) noexcept
        : balance_cents_{opening_cents >= 0 ? opening_cents : 0} {}

    [[nodiscard]] bool deposit(std::int64_t cents) noexcept {
        if (cents <= 0 || cents > std::numeric_limits<std::int64_t>::max() - balance_cents_) {
            return false;
        }
        balance_cents_ += cents;
        return true;
    }

    [[nodiscard]] bool withdraw(std::int64_t cents) noexcept {
        if (cents <= 0 || cents > balance_cents_) {
            return false;
        }
        balance_cents_ -= cents;
        return true;
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
