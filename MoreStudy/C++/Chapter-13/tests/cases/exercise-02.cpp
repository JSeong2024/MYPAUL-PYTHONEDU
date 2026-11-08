#include <cassert>
#include <concepts>
#include <type_traits>
#include CH13_SOURCE_PATH
static_assert(!std::is_convertible_v<Quantity<DistanceTag>,Quantity<TimeTag>>);
static_assert(!std::is_constructible_v<Quantity<TimeTag>,Quantity<DistanceTag>>);
int main() {
    const Quantity<DistanceTag> a{10}, b{25};
    assert((a+b).value() == 35);
    assert((Quantity<DistanceTag>{0}+b).value() == 25);
    const Quantity<TimeTag> t{7};
    assert(t.value() == 7);
}
