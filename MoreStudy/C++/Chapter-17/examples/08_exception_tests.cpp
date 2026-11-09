#include <iostream>
#include <stdexcept>
int parse_port(int port) {
    if (port < 1 || port > 65535) throw std::out_of_range("port");
    return port;
}
int main() {
    bool caught=false;
    try { (void)parse_port(0); }
    catch(const std::out_of_range&) { caught=true; }
    if (!caught || parse_port(8080)!=8080) throw std::runtime_error("error contract");
    std::cout << "Error contract: PASS\n";
}
