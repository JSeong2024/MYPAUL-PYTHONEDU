#include <iostream>

int main() {
    constexpr int item_count{17};
    constexpr int items_per_box{5};
    const int full_boxes{item_count / items_per_box};
    const int remaining{item_count % items_per_box};

    int packed_items{0};
    packed_items += full_boxes * items_per_box;

    std::cout << "Full boxes: " << full_boxes << '\n';
    std::cout << "Remaining items: " << remaining << '\n';
    std::cout << "Packed items: " << packed_items << '\n';
}
