#include <iostream>
#include <stdexcept>
#include <thread>
#include <vector>
#include CH14_SOURCE_PATH

void require(bool condition) { if (!condition) throw std::runtime_error("closing queue"); }
int main() {
    ClosingQueue queue;
    require(queue.push(11));
    require(queue.push(22));
    queue.close();
    require(!queue.push(33));
    require(queue.pop()==11);
    require(queue.pop()==22);
    require(!queue.pop().has_value());
    ClosingQueue waiting;
    bool woke=false;
    std::jthread consumer{[&] { woke=!waiting.pop().has_value(); }};
    waiting.close();
    consumer.join();
    require(woke);
    ClosingQueue multiple;
    std::vector<std::jthread> producers;
    for (int i=0;i<3;++i) producers.emplace_back([&multiple,i] {
        for (int j=0;j<50;++j) (void)multiple.push(i*100+j);
    });
    for (auto& t:producers) t.join();
    multiple.close();
    int count=0;long long sum=0;
    while (auto item=multiple.pop()) {++count;sum+=*item;}
    require(count==150 && sum==3LL*50*49/2+15000);
    std::cout << "PASS\n";
}
