#include <iostream>
#include <mutex>
#include <thread>
int main() {
    int counter=0;
    std::mutex guard;
    auto worker=[&]{for(int i=0;i<1000;++i){std::lock_guard lock{guard};++counter;}};
    std::thread a{worker}, b{worker};
    a.join();b.join();
    if(counter!=2000)return 1;
    std::cout << "Counter: " << counter << '\n';
}
