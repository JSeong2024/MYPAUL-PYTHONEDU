#include "prolink/api.hpp"
#include <iostream>
int main() {
    const auto result = prolink::round_trip("UPPER hello");
    if (!result) return 1;
    std::cout << "Reply: " << result.reply << '\n';
}
