#include <cassert>
#include <optional>
#include <string_view>
#include CH13_SOURCE_PATH
int main() {
    assert(parse_port("1")==1);
    assert(parse_port("65535")==65535);
    assert(parse_port("0080")==80);
    for (std::string_view s: {"","0","65536","-1","+2","80x"," 80","80 ","100000000000000000000000"}) {
        assert(!parse_port(s).has_value());
    }
}
