#include "prolink/api.hpp"
#include <stdexcept>
#include <string>
void check(bool b) { if (!b) throw std::runtime_error("SDK test failed"); }
int main() {
    check(prolink::process_command("PING") == "PONG");
    check(prolink::process_command("UPPER hello") == "HELLO");
    check(prolink::process_command("UPPER HELLO") == "ERR invalid text");
    check(prolink::process_command("BAD") == "ERR unknown command");
    check(!prolink::decode_packet("bad"));
    check(prolink::decode_packet(std::string{"\0\0\0\4PING",8}).value_or("") == "PING");
    check(!prolink::decode_packet(std::string{"\0\0\0\5PING",8}));
    const auto response = prolink::round_trip("UPPER hello");
    check(response && response.reply == "HELLO");
    check(prolink::round_trip("PING").reply == "PONG");
    check(prolink::round_trip("").error == prolink::Error::invalid_request);
    check(prolink::round_trip(std::string(4097, 'x')).error == prolink::Error::too_large);
}
