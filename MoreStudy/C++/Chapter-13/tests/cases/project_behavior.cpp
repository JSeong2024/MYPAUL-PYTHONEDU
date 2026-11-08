#include "telemetry/pipeline.hpp"
#include <array>
#include <cassert>
#include <cmath>
#include <limits>
#include <vector>
struct Sensor {
    double sample;
    bool okay;
    [[nodiscard]] double value() const { return sample; }
    [[nodiscard]] bool valid() const { return okay; }
};
static_assert(telemetry::ReadingLike<Sensor>);
static_assert(!telemetry::ReadingLike<int>);
int main() {
    const std::vector<Sensor> empty;
    assert(!telemetry::summarize(empty));
    const std::array readings{Sensor{10,true},Sensor{20,true},Sensor{30,true}};
    auto summary=telemetry::summarize(readings);
    assert(summary && summary->count==3);
    assert(summary->minimum==10 && summary->maximum==30);
    assert(std::abs(summary->average-20.0)<1e-12);
    const std::array corrupt{Sensor{std::numeric_limits<double>::quiet_NaN(),true},
                             Sensor{99,false},Sensor{7,true}};
    auto valid=telemetry::summarize(corrupt);
    assert(valid && valid->count==1 && valid->average==7);
}
