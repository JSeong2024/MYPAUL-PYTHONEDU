#include <iostream>

double rectangle_area(double width, double height) {
    return width * height;
}

int main() {
    std::cout << "Area: " << rectangle_area(2.5, 4.0) << " m2\n";
}
