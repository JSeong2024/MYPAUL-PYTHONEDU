#include "telemetry.hpp"
#include "../../../common/socket.hpp"
#include <charconv>
#include <exception>
#include <mutex>
#include <stdexcept>
#include <string>
#include <system_error>
#include <thread>
#include <vector>

namespace telemetry {
bool parse(std::string_view wire, std::string& device, int& value) {
    if (!wire.starts_with("READ ")) return false;
    wire.remove_prefix(5);
    const auto space = wire.find(' ');
    if (space == std::string_view::npos || space == 0 || space > 16) return false;
    const auto name = wire.substr(0, space);
    for (unsigned char c : name) {
        if (!((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') ||
              (c >= '0' && c <= '9') || c == '-' || c == '_')) return false;
    }
    wire.remove_prefix(space + 1);
    if (wire.empty()) return false;
    int parsed = 0;
    const auto [end, error] = std::from_chars(wire.data(), wire.data() + wire.size(), parsed);
    if (error != std::errc{} || end != wire.data() + wire.size() || parsed < 0 || parsed > 1000)
        return false;
    device = std::string{name};
    value = parsed;
    return true;
}
Result collect(const std::vector<std::string>& requests) {
    if (requests.size() > 32) throw std::invalid_argument("too many clients");
    for (const auto& request : requests)
        if (request.size() > lesson_net::max_payload) throw std::length_error("oversize request");
    if (requests.empty()) return {};
    lesson_net::Runtime runtime;
    std::uint16_t port = 0;
    const auto listener = lesson_net::listen_loopback(port, 32);
    std::mutex mutex;
    Result result{};
    std::exception_ptr server_failure;
    std::vector<std::exception_ptr> client_failures(requests.size());
    std::vector<std::string> replies(requests.size());
    std::thread server([&] {
        try {
            std::vector<std::jthread> handlers;
            for (std::size_t i = 0; i < requests.size(); ++i) {
                auto peer = lesson_net::accept_one(listener);
                handlers.emplace_back([&, p = std::move(peer)] () mutable {
                    try {
                        std::string input;
                        if (!lesson_net::receive_frame(p, input)) throw std::runtime_error("empty client");
                        std::string device;
                        int value = 0;
                        const bool good = parse(input, device, value);
                        {
                            std::lock_guard guard{mutex};
                            if (good) {
                                auto& aggregate = result.devices[device];
                                aggregate.count += 1;
                                aggregate.sum += value;
                                ++result.accepted;
                            } else ++result.rejected;
                        }
                        lesson_net::send_frame(p, good ? "OK" : "ERR invalid reading");
                    } catch (...) {
                        std::lock_guard guard{mutex};
                        if (!server_failure) server_failure = std::current_exception();
                    }
                });
            }
            // jthread destructors join all worker handlers before result is read.
        } catch (...) {
            std::lock_guard guard{mutex};
            if (!server_failure) server_failure = std::current_exception();
        }
    });
    std::vector<std::jthread> clients;
    for (std::size_t i = 0; i < requests.size(); ++i) {
        clients.emplace_back([&, i] {
            try {
                auto socket = lesson_net::connect_loopback(port);
                lesson_net::send_frame(socket, requests[i]);
                if (!lesson_net::receive_frame(socket, replies[i]))
                    throw std::runtime_error("missing server reply");
            } catch (...) { client_failures[i] = std::current_exception(); }
        });
    }
    clients.clear();
    server.join();
    if (server_failure) std::rethrow_exception(server_failure);
    for (const auto& e : client_failures) if (e) std::rethrow_exception(e);
    for (std::size_t i = 0; i < requests.size(); ++i) {
        const bool expected_ok = replies[i] == "OK";
        const bool expected_error = replies[i] == "ERR invalid reading";
        if (!expected_ok && !expected_error) throw std::runtime_error("bad server reply");
    }
    return result;
}
} // namespace telemetry
