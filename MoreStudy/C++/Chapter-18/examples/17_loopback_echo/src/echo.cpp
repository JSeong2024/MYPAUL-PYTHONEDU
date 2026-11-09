#include "echo.hpp"
#include "../../../common/socket.hpp"
#include <exception>
#include <stdexcept>
#include <thread>
namespace echo {
std::string round_trip(std::string_view message) {
    if (message.size() > lesson_net::max_payload)
        throw std::length_error("message exceeds protocol limit");
    lesson_net::Runtime runtime;
    std::uint16_t port = 0;
    const auto listener = lesson_net::listen_loopback(port);
    std::exception_ptr failure;
    std::thread server([&] {
        try {
            auto peer = lesson_net::accept_one(listener);
            std::string request;
            if (!lesson_net::receive_frame(peer, request)) throw std::runtime_error("missing request");
            lesson_net::send_frame(peer, request);
        } catch (...) { failure = std::current_exception(); }
    });
    try {
        auto client = lesson_net::connect_loopback(port);
        lesson_net::send_frame(client, message);
        std::string reply;
        if (!lesson_net::receive_frame(client, reply)) throw std::runtime_error("missing reply");
        server.join();
        if (failure) std::rethrow_exception(failure);
        return reply;
    } catch (...) {
        if (server.joinable()) server.join();
        throw;
    }
}
} // namespace echo
