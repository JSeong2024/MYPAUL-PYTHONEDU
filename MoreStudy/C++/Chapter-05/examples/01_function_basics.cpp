#include <print>

[[nodiscard]] double rectangle_area(double width, double height) noexcept {
    return width * height;
}

int main() {
    const double width{2.5};
    const double height{4.0};
    std::println("Area: {:.2f} m2", rectangle_area(width, height));
}
