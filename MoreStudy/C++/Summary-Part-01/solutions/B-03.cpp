#include <iomanip>
#include <iostream>
#include <vector>

int main() {
    int count = 0;
    if (!(std::cin >> count) || count < 1 || count > 100) {
        std::cout << "INVALID\n";
        return 0;
    }

    std::vector<int> scores;
    scores.reserve(static_cast<std::size_t>(count));
    for (int i = 0; i < count; ++i) {
        int score = 0;
        if (!(std::cin >> score) || score < 0 || score > 100) {
            std::cout << "INVALID\n";
            return 0;
        }
        scores.push_back(score);
    }

    int minimum = scores.front();
    int maximum = scores.front();
    int sum = 0;
    for (int score : scores) {
        if (score < minimum) minimum = score;
        if (score > maximum) maximum = score;
        sum += score;
    }
    std::cout << "MIN " << minimum << "\nMAX " << maximum << "\nAVG "
              << std::fixed << std::setprecision(1)
              << static_cast<double>(sum) / count << '\n';
}
