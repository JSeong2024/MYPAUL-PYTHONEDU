#include <iostream>
#include <string>

int main() {
    std::string name;
    std::string course;
    std::string goal;

    std::cout << "Name: ";
    std::getline(std::cin, name);
    std::cout << "Course: ";
    std::getline(std::cin, course);
    std::cout << "Goal: ";
    std::getline(std::cin, goal);

    std::cout << "\n--- Registration Card ---\n";
    std::cout << "Name: " << name << '\n';
    std::cout << "Course: " << course << '\n';
    std::cout << "Goal: " << goal << '\n';
    return 0;
}
