#include <print>

int main() {
    constexpr int item_count{17};
    constexpr int items_per_box{5};

    const int full_boxes{item_count / items_per_box};
    const int remainder{item_count % items_per_box};

    std::println("Full boxes: {}", full_boxes);
    std::println("Remaining items: {}", remainder);
}
