#include <cassert>
#include <memory>
#include <stdexcept>
#include <string>
#include CH12_SOURCE_PATH
int main() {
    DeviceRegistry registry;
    assert(!registry.has_device());
    auto first = std::make_unique<Device>(Device{"Motor-A"});
    registry.install(std::move(first));
    assert(first == nullptr);
    assert(registry.has_device());
    assert(registry.name() == "Motor-A");
    auto second = std::make_unique<Device>(Device{"Pump-B"});
    registry.install(std::move(second));
    assert(second == nullptr && registry.name() == "Pump-B");
    bool rejected = false;
    try { registry.install(nullptr); } catch (const std::invalid_argument&) { rejected = true; }
    assert(rejected && registry.name() == "Pump-B");
    rejected = false;
    try { registry.install(std::make_unique<Device>(Device{""})); }
    catch (const std::invalid_argument&) { rejected = true; }
    assert(rejected && registry.name() == "Pump-B");
}
