#include <cassert>
#include <stdexcept>
#include <vector>
#include CH12_SOURCE_PATH
int main() {
    SensorStore store{{10, 20}};
    const int valid[]{0, 100};
    store.replace(valid);
    assert((store.values() == std::vector<int>{0, 100}));
    for (const std::vector<int>& bad : {std::vector<int>{}, std::vector<int>{50, 101}, std::vector<int>{-1}}) {
        bool rejected = false;
        try { store.replace(bad); } catch (const std::invalid_argument&) { rejected = true; }
        assert(rejected);
        assert((store.values() == std::vector<int>{0, 100}));
    }
    const int one[]{27};
    store.replace(one);
    assert((store.values() == std::vector<int>{27}));
}
