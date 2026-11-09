#pragma once
// C++20 educational loopback TCP helper. Network operations are platform APIs,
// not part of the ISO C++20 standard library. No global using directives.
#include <array>
#include <cstdint>
#include <limits>
#include <stdexcept>
#include <string>
#include <string_view>
#include <utility>
#ifdef _WIN32
#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#include <winsock2.h>
#include <ws2tcpip.h>
#else
#include <arpa/inet.h>
#include <cerrno>
#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <unistd.h>
#endif

namespace lesson_net {
#ifdef _WIN32
using NativeSocket = SOCKET;
constexpr NativeSocket invalid_socket = INVALID_SOCKET;
#else
using NativeSocket = int;
constexpr NativeSocket invalid_socket = -1;
#endif
constexpr std::uint32_t max_payload = 4096;

class Runtime {
public:
    Runtime() {
#ifdef _WIN32
        WSADATA data{};
        if (WSAStartup(MAKEWORD(2, 2), &data) != 0)
            throw std::runtime_error("WSAStartup failed");
#endif
    }
    ~Runtime() {
#ifdef _WIN32
        WSACleanup();
#endif
    }
    Runtime(const Runtime&) = delete;
    Runtime& operator=(const Runtime&) = delete;
};

inline void close_native(NativeSocket socket) noexcept {
    if (socket == invalid_socket) return;
#ifdef _WIN32
    closesocket(socket);
#else
    ::close(socket);
#endif
}

class Socket {
public:
    Socket() noexcept = default;
    explicit Socket(NativeSocket raw) noexcept : fd_(raw) {}
    ~Socket() { close_native(fd_); }
    Socket(const Socket&) = delete;
    Socket& operator=(const Socket&) = delete;
    Socket(Socket&& other) noexcept : fd_(std::exchange(other.fd_, invalid_socket)) {}
    Socket& operator=(Socket&& other) noexcept {
        if (this != &other) {
            close_native(fd_);
            fd_ = std::exchange(other.fd_, invalid_socket);
        }
        return *this;
    }
    [[nodiscard]] NativeSocket get() const noexcept { return fd_; }
    [[nodiscard]] bool valid() const noexcept { return fd_ != invalid_socket; }
private:
    NativeSocket fd_{invalid_socket};
};

inline Socket tcp_socket() {
    NativeSocket fd = ::socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (fd == invalid_socket) throw std::runtime_error("socket failed");
    return Socket(fd);
}

inline void set_timeout(const Socket& socket, int milliseconds = 4000) {
    if (milliseconds <= 0) throw std::invalid_argument("timeout must be positive");
#ifdef _WIN32
    DWORD value = static_cast<DWORD>(milliseconds);
    auto* ptr = reinterpret_cast<const char*>(&value);
    constexpr int length = sizeof(value);
#else
    timeval value{milliseconds / 1000, (milliseconds % 1000) * 1000};
    auto* ptr = reinterpret_cast<const char*>(&value);
    constexpr socklen_t length = sizeof(value);
#endif
    if (::setsockopt(socket.get(), SOL_SOCKET, SO_RCVTIMEO, ptr, length) != 0 ||
        ::setsockopt(socket.get(), SOL_SOCKET, SO_SNDTIMEO, ptr, length) != 0)
        throw std::runtime_error("setsockopt timeout failed");
}

inline sockaddr_in loopback_address(std::uint16_t port) {
    sockaddr_in address{};
    address.sin_family = AF_INET;
    address.sin_port = htons(port);
    address.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    return address;
}

inline Socket listen_loopback(std::uint16_t& bound_port, int backlog = 8) {
    Socket server = tcp_socket();
    const auto address = loopback_address(0); // use an ephemeral port: no fixed-port conflict
    if (::bind(server.get(), reinterpret_cast<const sockaddr*>(&address), sizeof(address)) != 0 ||
        ::listen(server.get(), backlog) != 0)
        throw std::runtime_error("bind/listen failed");
    sockaddr_in actual{};
#ifdef _WIN32
    int size = sizeof(actual);
#else
    socklen_t size = sizeof(actual);
#endif
    if (::getsockname(server.get(), reinterpret_cast<sockaddr*>(&actual), &size) != 0)
        throw std::runtime_error("getsockname failed");
    bound_port = ntohs(actual.sin_port);
    set_timeout(server);
    return server;
}

inline Socket connect_loopback(std::uint16_t port) {
    Socket client = tcp_socket();
    set_timeout(client);
    const auto address = loopback_address(port);
    if (::connect(client.get(), reinterpret_cast<const sockaddr*>(&address), sizeof(address)) != 0)
        throw std::runtime_error("connect failed");
    return client;
}

inline Socket accept_one(const Socket& server) {
    const NativeSocket fd = ::accept(server.get(), nullptr, nullptr);
    if (fd == invalid_socket) throw std::runtime_error("accept failed or timed out");
    Socket incoming{fd};
    set_timeout(incoming);
    return incoming;
}

inline void send_all(const Socket& socket, std::string_view bytes) {
    std::size_t sent = 0;
    while (sent < bytes.size()) {
        const auto left = bytes.size() - sent;
        const auto length = static_cast<int>(left < 16384 ? left : 16384);
        int flags = 0;
#ifdef MSG_NOSIGNAL
        flags = MSG_NOSIGNAL;
#endif
        const int result = ::send(socket.get(), bytes.data() + sent, length, flags);
        if (result <= 0) throw std::runtime_error("send failed/peer closed");
        sent += static_cast<std::size_t>(result);
    }
}

// False only for a clean EOF before a new frame; partial EOF is an error.
inline bool recv_exact(const Socket& socket, char* out, std::size_t size) {
    std::size_t have = 0;
    while (have < size) {
        const auto left = size - have;
        const auto length = static_cast<int>(left < 16384 ? left : 16384);
        const int n = ::recv(socket.get(), out + have, length, 0);
        if (n == 0 && have == 0) return false;
        if (n <= 0) throw std::runtime_error("recv failed/truncated frame");
        have += static_cast<std::size_t>(n);
    }
    return true;
}

inline std::string encode_frame(std::string_view payload) {
    if (payload.size() > max_payload) throw std::length_error("frame exceeds 4096 bytes");
    const std::uint32_t size = static_cast<std::uint32_t>(payload.size());
    std::string encoded(4, '\0');
    encoded[0] = static_cast<char>((size >> 24) & 0xff);
    encoded[1] = static_cast<char>((size >> 16) & 0xff);
    encoded[2] = static_cast<char>((size >> 8) & 0xff);
    encoded[3] = static_cast<char>(size & 0xff);
    encoded.append(payload);
    return encoded;
}

inline void send_frame(const Socket& socket, std::string_view payload) {
    send_all(socket, encode_frame(payload));
}
inline bool receive_frame(const Socket& socket, std::string& output) {
    std::array<char, 4> header{};
    if (!recv_exact(socket, header.data(), header.size())) return false;
    std::uint32_t size = 0;
    for (unsigned char byte : header) size = (size << 8) | byte;
    if (size > max_payload) throw std::length_error("frame length exceeds 4096");
    std::string buffer(size, '\0');
    if (size && !recv_exact(socket, buffer.data(), size))
        throw std::runtime_error("truncated frame payload");
    output = std::move(buffer);
    return true;
}
} // namespace lesson_net
