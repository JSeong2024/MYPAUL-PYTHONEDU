#ifndef MORESTUDY_CPP_CHAPTER_08_DEVICE_REGISTRY_HPP
#define MORESTUDY_CPP_CHAPTER_08_DEVICE_REGISTRY_HPP

#include <cstddef>
#include <string>
#include <string_view>
#include <vector>

class DeviceRegistry {
public:
    [[nodiscard]] bool add(std::string id);
    [[nodiscard]] bool contains(std::string_view id) const;
    [[nodiscard]] std::size_t size() const noexcept;

private:
    std::vector<std::string> ids_;
};

#endif
