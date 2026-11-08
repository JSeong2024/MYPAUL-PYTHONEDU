#include <cassert>
#include <stdexcept>
#include <utility>
#include <variant>
#include "session.hpp"
int main() {
    assert(demo::closed_count() == 0);
    auto invalid = demo::Session::open("");
    assert(std::holds_alternative<demo::OpenError>(invalid));
    assert(std::get<demo::OpenError>(invalid) == demo::OpenError::empty_id);
    auto offline = demo::Session::open("offline");
    assert(std::get<demo::OpenError>(offline) == demo::OpenError::unavailable);
    assert(demo::closed_count() == 0);
    {
        auto result = demo::Session::open("sensor-A");
        assert(std::holds_alternative<demo::Session>(result));
        demo::Session original{std::move(std::get<demo::Session>(result))};
        assert(original.name() == "sensor-A");
        assert(original.next_reading() == 21);
        demo::Session other{std::move(original)};
        assert(original.name().empty());
        bool threw = false;
        try { (void)original.next_reading(); }
        catch (const std::logic_error&) { threw = true; }
        assert(threw);
        assert(other.next_reading() == 24);
        assert(other.next_reading() == 22);
        assert(other.next_reading() == 21);
        assert(demo::closed_count() == 0);
    }
    assert(demo::closed_count() == 1);
    {
        auto result = demo::Session::open("sensor-B");
        assert(std::holds_alternative<demo::Session>(result));
    }
    assert(demo::closed_count() == 2);
}
