#include <cassert>
#include <cmath>
#include <concepts>
#include <limits>
#include CH13_SOURCE_PATH

template <typename T>
concept CanAlert = requires(T v) { reading_alert(v, v); };
static_assert(CanAlert<float> && CanAlert<double>);
static_assert(!CanAlert<int>);
int main() {
    assert(reading_alert(80.0,80.0));
    assert(!reading_alert(79.9,80.0));
    assert(reading_alert(81.2f,80.0f));
    assert(!reading_alert(std::numeric_limits<double>::quiet_NaN(),80.0));
    assert(!reading_alert(90.0,std::numeric_limits<double>::infinity()));
    assert(!reading_alert(-std::numeric_limits<double>::infinity(),80.0));
}
