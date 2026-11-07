#include <cstdint>
#include <limits>
#include <print>

class BankAccount {
public:
    explicit BankAccount(std::int64_t opening_cents) noexcept
        : balance_cents_{opening_cents >= 0 ? opening_cents : 0} {}

    [[nodiscard]] bool deposit(std::int64_t amount_cents) noexcept {
        if (amount_cents <= 0 ||
            balance_cents_ > std::numeric_limits<std::int64_t>::max() - amount_cents) {
            return false;
        }
        balance_cents_ += amount_cents;
        return true;
    }

    [[nodiscard]] bool withdraw(std::int64_t amount_cents) noexcept {
        if (amount_cents <= 0 || amount_cents > balance_cents_) {
            return false;
        }
        balance_cents_ -= amount_cents;
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
    const bool deposited = account.deposit(2'500);
    const bool withdrawn = account.withdraw(4'000);
    std::println("Deposit: {}, withdraw: {}, balance: {} cents",
                 deposited, withdrawn, account.balance_cents());
}
