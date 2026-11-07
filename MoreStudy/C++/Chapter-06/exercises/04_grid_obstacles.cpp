#include <iostream>
#include <print>
#include <string>
#include <vector>

int main() {
    // 첫 줄: W H (각 1~30)
    // 다음 H줄: 정확히 W개의 '.'(빈 공간) 또는 '#'(장애물)
    int width{}, height{};
    if (!(std::cin >> width >> height) || width < 1 || width > 30 ||
        height < 1 || height > 30) {
        std::println(stderr, "Invalid grid size");
        return 1;
    }

    std::vector<std::string> grid;
    // TODO: H개 행을 읽고 길이와 문자를 검증함.
    // TODO: 장애물 수, 빈 공간 수, 경계의 장애물 유무를 출력함.
    // 출력: Grid / Blocked / Free / All borders clear (yes/no)
    std::println("TODO: implement grid analysis");
}
