#include <functional>
#include <print>
#include <string>
#include <utility>

template <typename F, typename... Args>
decltype(auto) call(F&& function, Args&&... args) {
    return std::invoke(std::forward<F>(function),
                       std::forward<Args>(args)...);
}

struct Logger {
    void show(const std::string& text) const { std::println("Log: {}", text); }
};

int main() {
    Logger logger;
    call(&Logger::show, logger, std::string{"ready"});
    const auto result = call([](int a, int b) { return a + b; }, 3, 5);
    std::println("Result: {}", result);
}
