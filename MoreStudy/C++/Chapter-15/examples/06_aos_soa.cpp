#include <iostream>
#include <vector>

struct Reading { int device_id; int value; };
int main() {
    const std::vector<Reading> rows{{1, 10}, {2, 20}, {3, 30}};
    std::vector<int> ids;
    std::vector<int> values;
    ids.reserve(rows.size());
    values.reserve(rows.size());
    for (const Reading& item : rows) {
        ids.push_back(item.device_id);
        values.push_back(item.value);
    }
    int sum = 0;
    for (const int value : values) sum += value;
    std::cout << "Rows: " << ids.size() << ", Sum: " << sum << "\n";
}
