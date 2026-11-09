#include "prolink/api.hpp"
#include "../../../common/socket.hpp"
#include <cstdint>
#include <exception>
#include <stdexcept>
#include <thread>
namespace prolink {
std::string process_command(std::string_view command) {
    if (command == "PING") return "TODO"; // TODO: implement PING response
    if (command.starts_with("UPPER ") && command.size() > 6 && command.size() <= 38) {
        std::string output(command.substr(6));
        for (char& c : output) {
            if (c < 'a' || c > 'z') return "ERR invalid text";
            c = static_cast<char>(c - 'a' + 'A');
        }
        return output;
    }
    if (command == "UPPER ") return "ERR invalid text";
    return "ERR unknown command";
}
std::optional<std::string> decode_packet(std::string_view packet) {
    if (packet.size() < 4) return std::nullopt;
    std::uint32_t size = 0;
    for (std::size_t i = 0; i < 4; ++i)
        size = (size << 8) | static_cast<unsigned char>(packet[i]);
    if (size > lesson_net::max_payload || packet.size() - 4 != size) return std::nullopt;
    return std::string(packet.substr(4));
}
Result round_trip(std::string_view command) {
    if (command.size() > lesson_net::max_payload) return {"", Error::too_large};
    if (command.empty()) return {"", Error::invalid_request};
    try {
        lesson_net::Runtime runtime;
        std::uint16_t port = 0;
        const auto listener = lesson_net::listen_loopback(port);
        std::exception_ptr server_failure;
        std::thread server([&] {
            try {
                auto peer = lesson_net::accept_one(listener);
                std::string request;
                if (!lesson_net::receive_frame(peer, request)) throw std::runtime_error("missing request");
                lesson_net::send_frame(peer, process_command(request));
            } catch (...) { server_failure = std::current_exception(); }
        });
        try {
            auto client = lesson_net::connect_loopback(port);
            lesson_net::send_frame(client, command);
            std::string response;
            if (!lesson_net::receive_frame(client, response)) throw std::runtime_error("missing response");
            server.join();
            if (server_failure) std::rethrow_exception(server_failure);
            return {std::move(response), Error::none};
        } catch (...) {
            if (server.joinable()) server.join();
            throw;
        }
    } catch (...) { return {"", Error::transport}; }
}
} // namespace prolink
