#include <iostream>

class Connection {
public:
    Connection() noexcept { ++active_; }
    ~Connection() { --active_; }

    Connection(const Connection&) = delete;
    Connection& operator=(const Connection&) = delete;
    Connection(Connection&&) = delete;
    Connection& operator=(Connection&&) = delete;

    [[nodiscard]] static int active_count() noexcept { return active_; }

private:
    inline static int active_{0};
};

int main() {
    std::cout << "Before: " << Connection::active_count() << '\n';
    {
        Connection first;
        Connection second;
        std::cout << "Inside: " << Connection::active_count() << '\n';
    }
    std::cout << "After: " << Connection::active_count() << '\n';
}
