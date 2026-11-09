#include "dispatch/dispatcher.hpp"
#include <stdexcept>

namespace dispatch {
Dispatcher::Dispatcher(std::size_t worker_count) {
    if (worker_count == 0 || worker_count > 32)
        throw std::invalid_argument("worker_count must be 1..32");
    // TODO: worker_count개의 소비자 스레드를 생성하세요.
}
Dispatcher::~Dispatcher() { (void)finish(); }

bool Dispatcher::submit(Sample sample) {
    // TODO: 작업 유효성 검증, 큐 삽입, 알림, 집계.
    (void)sample;
    return false;
}
void Dispatcher::consume() {
    // TODO: 조건 변수와 큐를 사용하여 종료 신호까지 처리.
}
Summary Dispatcher::snapshot() const {
    std::lock_guard lock{mutex_};
    return summary_;
}
Summary Dispatcher::finish() {
    // TODO: 추가 제출을 차단한 다음 남은 큐를 비우고 join.
    return snapshot();
}
} // namespace dispatch
