#include <condition_variable>
#include <deque>
#include <iostream>
#include <mutex>
#include <optional>
#include <thread>

class ClosingQueue {
public:
    [[nodiscard]] bool push(int value) {
        // TODO: 닫힌 큐는 거부합니다. 그 외에는 삽입 후 소비자를 알립니다.
        (void)value;
        return false;
    }
    [[nodiscard]] std::optional<int> pop() {
        // TODO: 조건 변수의 predicate로 대기하고, 남은 데이터를 먼저 반환합니다.
        // 큐가 닫히고 비어 있으면 std::nullopt를 반환합니다.
        return std::nullopt;
    }
    void close() {
        // TODO: 종료 상태를 설정하고 대기 중인 모든 소비자를 깨웁니다.
    }
private:
    std::mutex mutex_;
    std::condition_variable changed_;
    std::deque<int> data_;
    bool closed_ = false;
};

#ifndef CH14_LIBRARY_ONLY
int main() {
    ClosingQueue queue;
    (void)queue.push(11);
    (void)queue.push(22);
    queue.close();
    const auto a = queue.pop();
    const auto b = queue.pop();
    const auto end = queue.pop();
    std::cout << "Values: " << a.value_or(-1) << ", " << b.value_or(-1)
              << ", Closed: " << std::boolalpha << !end.has_value() << '\n';
}
#endif
