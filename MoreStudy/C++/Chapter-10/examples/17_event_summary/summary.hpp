#ifndef MORESTUDY_CHAPTER_10_EVENT_SUMMARY_HPP
#define MORESTUDY_CHAPTER_10_EVENT_SUMMARY_HPP

#include <cstddef>
#include <map>
#include <string>
#include <string_view>

namespace events {

struct Summary {
    std::map<std::string, int> frequency;
    int total{};
};

[[nodiscard]] bool add_event(Summary& report, std::string_view name);
[[nodiscard]] std::size_t distinct_count(const Summary& report) noexcept;

}  // namespace events

#endif
