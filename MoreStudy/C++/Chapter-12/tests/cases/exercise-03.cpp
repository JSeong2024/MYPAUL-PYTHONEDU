#include <cassert>
#include <type_traits>
#include <utility>
#include CH12_SOURCE_PATH
int main() {
    static_assert(!std::is_copy_constructible_v<Packet>);
    static_assert(std::is_nothrow_move_constructible_v<Packet>);
    Packet first{{2, 3, 5}};
    assert(first.size() == 3 && first.sum() == 10);
    Packet second{std::move(first)};
    assert(second.size() == 3 && second.sum() == 10);
    assert(first.size() == 0 && first.sum() == 0);
    Packet third{{9}};
    third = std::move(second);
    assert(third.size() == 3 && third.sum() == 10);
    assert(second.size() == 0 && second.sum() == 0);
    Packet empty{{}};
    assert(empty.size() == 0 && empty.sum() == 0);
}
