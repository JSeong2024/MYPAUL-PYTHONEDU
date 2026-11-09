#include <chrono>
#include <future>
#include <stdexcept>
#include <thread>
void check(bool v) { if (!v) throw std::runtime_error("queue behavior error"); }
int main() {
 BoundedQueue q{1};
 check(q.push(11));
 std::promise<bool> accepted;
 auto answer = accepted.get_future();
 std::thread producer([&]{ accepted.set_value(q.push(22)); });
 // Full queue: 2nd producer is blocked until first item is drained.
 check(q.pop().value_or(-1) == 11);
 check(answer.wait_for(std::chrono::seconds(2)) == std::future_status::ready);
 check(answer.get());
 producer.join();
 q.close();
 check(q.pop().value_or(-1) == 22);
 check(!q.pop());
 check(!q.push(33));
 BoundedQueue pending{1};
 check(pending.push(99));
 std::promise<bool> done;
 auto future = done.get_future();
 std::thread writer([&]{ done.set_value(pending.push(100)); });
 pending.close();
 check(future.wait_for(std::chrono::seconds(2)) == std::future_status::ready);
 check(!future.get());
 writer.join();
 check(pending.pop().value_or(-1) == 99);
 check(!pending.pop());
 try{ BoundedQueue invalid{0}; }catch(const std::invalid_argument&){return 0;}
 return 1;
}
