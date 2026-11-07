#ifndef MORESTUDY_CHAPTER_05_INVENTORY_HPP
#define MORESTUDY_CHAPTER_05_INVENTORY_HPP

#include <optional>

namespace inventory {

[[nodiscard]] std::optional<int>
remaining_stock(int received, int shipped) noexcept;

}  // namespace inventory

#endif
