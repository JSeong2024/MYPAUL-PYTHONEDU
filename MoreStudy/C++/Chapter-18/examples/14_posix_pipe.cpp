#include <iostream>
#ifndef _WIN32
#include <array>
#include <stdexcept>
#include <sys/wait.h>
#include <unistd.h>
#endif
int main() {
#ifdef _WIN32
    std::cout << "POSIX pipe requires a POSIX system\n";
#else
    int fds[2]{};
    if (::pipe(fds) == -1) throw std::runtime_error("pipe failed");
    const pid_t pid = ::fork();
    if (pid < 0) { ::close(fds[0]); ::close(fds[1]); throw std::runtime_error("fork failed"); }
    if (pid == 0) {
        ::close(fds[0]);
        constexpr char message[] = "from child";
        const auto n = ::write(fds[1], message, sizeof(message) - 1);
        ::close(fds[1]);
        _exit(n == static_cast<ssize_t>(sizeof(message) - 1) ? 0 : 1);
    }
    ::close(fds[1]);
    std::array<char, 32> buffer{};
    const auto n = ::read(fds[0], buffer.data(), buffer.size());
    ::close(fds[0]);
    int status = 0;
    if (::waitpid(pid, &status, 0) != pid || !WIFEXITED(status) || WEXITSTATUS(status) != 0 || n < 0)
        throw std::runtime_error("child IPC failed");
    std::cout << "IPC: " << std::string(buffer.data(), static_cast<std::size_t>(n)) << '\n';
#endif
}
