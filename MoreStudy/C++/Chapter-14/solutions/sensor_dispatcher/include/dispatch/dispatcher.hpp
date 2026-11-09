#pragma once

#include <condition_variable>
#include <cstddef>
#include <deque>
#include <mutex>
#include <thread>
#include <vector>

namespace dispatch {
struct Sample {
    int device_id{};
    int value{};
};
struct Summary {
    std::size_t accepted{};
    std::size_t processed{};
    std::size_t rejected{};
    std::size_t alerts{};
    long long checksum{};
};

// submit()은 여러 스레드에서 호출할 수 있다.
// finish()는 제출이 끝난 뒤 소유 스레드가 호출한다.
class Dispatcher {
public:
    explicit Dispatcher(std::size_t worker_count);
    ~Dispatcher();
    Dispatcher(const Dispatcher&) = delete;
    Dispatcher& operator=(const Dispatcher&) = delete;
    Dispatcher(Dispatcher&&) = delete;
    Dispatcher& operator=(Dispatcher&&) = delete;

    [[nodiscard]] bool submit(Sample sample);
    [[nodiscard]] Summary finish();
    [[nodiscard]] Summary snapshot() const;

private:
    void consume();
    mutable std::mutex mutex_;
    std::condition_variable changed_;
    std::deque<Sample> pending_;
    bool accepting_{true};
    Summary summary_{};
    std::vector<std::jthread> workers_;
};
} // namespace dispatch
