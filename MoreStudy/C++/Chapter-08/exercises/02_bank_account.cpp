#include <cstdint>
#include <print>

class BankAccount {
public:
    explicit BankAccount(std::int64_t opening_cents) noexcept
        : balance_cents_{opening_cents >= 0 ? opening_cents : 0} {}

    [[nodiscard]] bool deposit(std::int64_t amount_cents) noexcept {
        // TODO: 양수만 허용하고 정수 오버플로를 방지하면서 입금
        (void)amount_cents;
        return false;
    }

    [[nodiscard]] bool withdraw(std::int64_t amount_cents) noexcept {
        // TODO: 양수이고 현재 잔액 이내인 경우에만 출금
        (void)amount_cents;
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
    const bool deposited = account.deposit(2'500);
    const bool withdrawn = account.withdraw(4'000);
    std::println("Deposit: {}, withdraw: {}, balance: {} cents",
                 deposited, withdrawn, account.balance_cents());
}
