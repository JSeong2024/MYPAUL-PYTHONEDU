#include <prolink/api.hpp>
#include <iostream>
int main() {
    const auto result = prolink::round_trip("PING");
    if (!result || result.reply != "PONG") return 1;
    std::cout << "Installed SDK: " << result.reply << '\n';
}
