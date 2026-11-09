#include <iostream>
#include <string>

[[nodiscard]] std::string versioned_name(const std::string& name, int major) {
    // TODO: "name-v번호"를 반환. name은 비어 있으면 안 되고, major는 1 이상이어야 함.
    (void)name; (void)major;
    return {};
}
#ifndef CH16_LIBRARY_ONLY
int main() { std::cout << versioned_name("motor", 2) << '\n'; }
#endif
