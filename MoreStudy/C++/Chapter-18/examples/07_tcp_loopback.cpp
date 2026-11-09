#include "../common/socket.hpp"
#include <iostream>
#include <thread>
#include <exception>
int main() {
    lesson_net::Runtime runtime;
    std::uint16_t port = 0;
    const auto listener = lesson_net::listen_loopback(port);
    std::exception_ptr server_error;
    std::thread server([&] {
        try {
            auto peer = lesson_net::accept_one(listener);
            std::string value;
            if (!lesson_net::receive_frame(peer, value)) throw std::runtime_error("no message");
            lesson_net::send_frame(peer, "ECHO:" + value);
        } catch (...) { server_error = std::current_exception(); }
    });
    try {
        auto client = lesson_net::connect_loopback(port);
        lesson_net::send_frame(client, "hello");
        std::string reply;
        if (!lesson_net::receive_frame(client, reply)) throw std::runtime_error("no reply");
        server.join();
        if (server_error) std::rethrow_exception(server_error);
        std::cout << "Reply: " << reply << '\n';
    } catch (...) {
        if (server.joinable()) server.join();
        throw;
    }
}
