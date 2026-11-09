#include <iostream>
enum class Failure { timeout, unavailable, invalid_request, rejected };
// attempt: current failed attempt, starting at 1; max_attempts: total ceiling.
[[nodiscard]] bool should_retry(Failure reason, int attempt, int max_attempts) {
    if (attempt < 1 || max_attempts < 1 || attempt >= max_attempts) return false;
    return reason == Failure::timeout || reason == Failure::unavailable;
}
#ifndef CH18_LIBRARY_ONLY
int main() {
    std::cout << std::boolalpha
              << should_retry(Failure::timeout, 1, 3) << '\n'
              << should_retry(Failure::invalid_request, 1, 3) << '\n';
}
#endif
