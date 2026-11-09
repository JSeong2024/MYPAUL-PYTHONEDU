#include "dispatch/dispatcher.hpp"
#include <iostream>

int main() {
    dispatch::Dispatcher dispatcher{3};
    (void)dispatcher.submit({1, 55});
    (void)dispatcher.submit({2, 92});
    (void)dispatcher.submit({3, 80});
    (void)dispatcher.submit({0, 50}); // 잘못된 장치 ID: 거부
    (void)dispatcher.submit({4, 25});
    const auto result = dispatcher.finish();
    std::cout << "Accepted: " << result.accepted << '\n';
    std::cout << "Processed: " << result.processed << '\n';
    std::cout << "Rejected: " << result.rejected << '\n';
    std::cout << "Alerts: " << result.alerts << '\n';
    std::cout << "Checksum: " << result.checksum << '\n';
}
