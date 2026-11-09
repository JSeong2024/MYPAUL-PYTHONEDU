#include <iostream>
#ifndef _WIN32
#include <stdexcept>
#include <sys/socket.h>
#include <unistd.h>
#endif
int main() {
#ifdef _WIN32
    std::cout << "socketpair demonstration requires POSIX\n";
#else
    int handles[2]{};
    if (::socketpair(AF_UNIX, SOCK_STREAM, 0, handles) != 0)
        throw std::runtime_error("socketpair failed");
    constexpr char message[] = "LOCAL";
    const auto sent = ::send(handles[0], message, 5, 0);
    char buffer[16]{};
    const auto received = sent == 5 ? ::recv(handles[1], buffer, sizeof(buffer), 0) : -1;
    ::close(handles[0]);
    ::close(handles[1]);
    if (received != 5) throw std::runtime_error("local IPC failed");
    std::cout << "Local socket: " << std::string(buffer, 5) << '\n';
#endif
}
