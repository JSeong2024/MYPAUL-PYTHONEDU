#include <iostream>
#include <string_view>
int main(int argc,char** argv) {
    if(argc>1 && std::string_view{argv[1]}=="--self-test") {
        const int actual=2+3;
        if(actual!=5) return 1;
        std::cout << "Self-test: PASS\n";
        return 0;
    }
    std::cout << "Use --self-test\n";
}
