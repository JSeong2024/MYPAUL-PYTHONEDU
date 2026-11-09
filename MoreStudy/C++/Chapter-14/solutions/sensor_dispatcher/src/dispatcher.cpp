#include "dispatch/dispatcher.hpp"
#include <stdexcept>

namespace dispatch {
Dispatcher::Dispatcher(std::size_t worker_count) {
    if (worker_count == 0 || worker_count > 32)
        throw std::invalid_argument("worker_count must be 1..32");
    try {
        for (std::size_t i = 0; i < worker_count; ++i)
            workers_.emplace_back([this] { consume(); });
    } catch (...) {
        {
            std::lock_guard lock{mutex_};
            accepting_ = false;
        }
        changed_.notify_all();
        for (auto& worker : workers_) worker.join();
        throw;
    }
}

Dispatcher::~Dispatcher() {
    (void)finish();
}

bool Dispatcher::submit(Sample sample) {
    std::lock_guard lock{mutex_};
    if (!accepting_) return false;
    if (sample.device_id < 1 || sample.device_id > 10000 ||
        sample.value < 0 || sample.value > 100) {
        ++summary_.rejected;
        return false;
    }
    pending_.push_back(sample); // 할당 실패 시 큐와 카운터를 변경하지 않는다.
    ++summary_.accepted;
    changed_.notify_one();
    return true;
}

void Dispatcher::consume() {
    for (;;) {
        Sample sample;
        {
            std::unique_lock lock{mutex_};
            changed_.wait(lock, [this] { return !pending_.empty() || !accepting_; });
            if (pending_.empty()) return; // 닫혀도 남은 작업을 모두 처리한다.
            sample = pending_.front();
            pending_.pop_front();
        }
        const long long contribution =
            static_cast<long long>(sample.device_id) * 1000 + sample.value;
        {
            std::lock_guard lock{mutex_};
            ++summary_.processed;
            if (sample.value >= 80) ++summary_.alerts;
            summary_.checksum += contribution;
        }
    }
}

Summary Dispatcher::snapshot() const {
    std::lock_guard lock{mutex_};
    return summary_;
}

Summary Dispatcher::finish() {
    {
        std::lock_guard lock{mutex_};
        accepting_ = false;
    }
    changed_.notify_all();
    for (auto& worker : workers_) {
        if (worker.joinable()) worker.join();
    }
    workers_.clear();
    return snapshot();
}
} // namespace dispatch
