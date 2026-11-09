#include CH15_SOURCE_PATH
#include <array>
#include <stdexcept>

static void check(bool test) { if (!test) throw std::runtime_error("test failed"); }
int main() {
    std::pmr::monotonic_buffer_resource arena;
    std::pmr::vector<int> output{&arena};
    output.push_back(99);
    const std::array data{-1, 0, 50, 100, 101};
    ch15::append_valid(output, data);
    check((output == std::pmr::vector<int>{99, 0, 50, 100}));
    check(output.get_allocator().resource() == &arena);
    const std::array<int, 0> empty{};
    ch15::append_valid(output, empty);
    check(output.size() == 4);
    std::cout << "PASS\n";
}
