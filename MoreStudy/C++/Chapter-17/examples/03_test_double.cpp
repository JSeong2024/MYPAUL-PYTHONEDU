#include <iostream>
#include <stdexcept>
struct Source { virtual ~Source() = default; virtual int read() = 0; };
struct FakeSource final : Source { int read() override { return 85; } };
bool is_alert(Source& source) { return source.read() >= 80; }
int main() {
    FakeSource fake;
    if (!is_alert(fake)) throw std::runtime_error("fake input");
    std::cout << "Alert: true\n";
}
