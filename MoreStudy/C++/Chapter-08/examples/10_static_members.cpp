#include <print>

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
    std::println("Before: {}", Connection::active_count());
    {
        Connection first;
        Connection second;
        std::println("Inside: {}", Connection::active_count());
    }
    std::println("After: {}", Connection::active_count());
}
