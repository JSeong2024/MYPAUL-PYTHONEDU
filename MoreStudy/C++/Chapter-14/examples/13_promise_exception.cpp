#include <future>
#include <iostream>
#include <stdexcept>
#include <thread>
#include <utility>

int main() {
    std::promise<int> promise;
    auto result = promise.get_future();
    std::jthread producer{[p = std::move(promise)]() mutable {
        p.set_exception(std::make_exception_ptr(std::runtime_error{"sensor offline"}));
    }};
    try {
        (void)result.get();
    } catch (const std::runtime_error& error) {
        std::cout << "Error: " << error.what() << '\n';
    }
}
