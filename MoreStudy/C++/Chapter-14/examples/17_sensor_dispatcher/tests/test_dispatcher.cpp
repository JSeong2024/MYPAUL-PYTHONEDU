#include "dispatch/dispatcher.hpp"
#include <stdexcept>

void require(bool condition) {
    if (!condition) throw std::runtime_error("dispatcher behavior mismatch");
}
#include <stdexcept>
#include <thread>
#include <vector>

int main() {
    dispatch::Dispatcher queue{4};
    require(!queue.submit({0, 25}));
    require(!queue.submit({1, 101}));
    require(queue.submit({1, 10}));
    require(queue.submit({2, 80}));
    require(queue.submit({3, 100}));
    const auto result = queue.finish();
    require(result.accepted == 3);
    require(result.processed == 3);
    require(result.rejected == 2);
    require(result.alerts == 2);
    require(result.checksum == 1010 + 2080 + 3100); // 순서와 무관한 합계
    require(queue.finish().processed == 3);
    require(!queue.submit({2, 10}));

    dispatch::Dispatcher concurrent{4};
    std::vector<std::jthread> producers;
    for (int id = 1; id <= 4; ++id) {
        producers.emplace_back([&concurrent, id] {
            for (int j = 0; j < 300; ++j) {
                if (!concurrent.submit({id, 80}))
                    throw std::runtime_error("valid submit failed");
            }
        });
    }
    for (auto& worker : producers) worker.join();
    const auto total = concurrent.finish();
    require(total.accepted == 1200);
    require(total.processed == 1200);
    require(total.rejected == 0);
    require(total.alerts == 1200);
    require(total.checksum == 300LL * (1080 + 2080 + 3080 + 4080));
    bool invalid = false;
    try { dispatch::Dispatcher bad{0}; }
    catch (const std::invalid_argument&) { invalid = true; }
    require(invalid);
}
