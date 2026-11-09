#include <iostream>
enum class Failure { timeout, unavailable, invalid_request, rejected };
// TODO: retry only transient errors, with 1-based attempts and a hard attempt limit.
[[nodiscard]] bool should_retry(Failure reason, int attempt, int max_attempts) {
    (void)reason; (void)attempt; (void)max_attempts;
    return false;
}
#ifndef CH18_LIBRARY_ONLY
int main() {
    std::cout << std::boolalpha
              << should_retry(Failure::timeout, 1, 3) << '\n'
              << should_retry(Failure::invalid_request, 1, 3) << '\n';
}
#endif
