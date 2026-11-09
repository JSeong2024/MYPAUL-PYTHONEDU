#include <charconv>
#include <optional>
#include <string_view>
std::optional<int> parse_count(std::string_view text) {
    if(text.empty()) return std::nullopt;
    int result=0;
    const auto [end,ec]=std::from_chars(text.data(),text.data()+text.size(),result);
    if(ec!=std::errc{} || end!=text.data()+text.size() || result<0) return std::nullopt;
    return result;
}
#ifndef CH17_LIBRARY_ONLY
#include <iostream>
int main(){auto n=parse_count("42");std::cout << "Count: " << (n?*n:-1) << '\n';}
#endif
