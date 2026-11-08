#include <algorithm>
#include <iostream>
#include <ranges>
#include <string>
#include <vector>

struct Device {
    std::string id;
    int reading;
    bool active;
};

[[nodiscard]] std::vector<Device> selected_devices(const std::vector<Device>& source,
                                                    int threshold) {
    // TODO: active == true 이고 reading >= threshold인 장치만 선택
    // TODO: 결과를 id 오름차순으로 정렬 (projection 또는 comparator)
    (void)source;
    (void)threshold;
    return {};
}

#ifndef CH13_LIBRARY_ONLY
int main() {
    const std::vector<Device> data{{"B", 80, true}, {"A", 90, true}, {"C", 99, false}};
    for (const auto& d : selected_devices(data, 80)) std::cout << d.id << '\n';
}
#endif
