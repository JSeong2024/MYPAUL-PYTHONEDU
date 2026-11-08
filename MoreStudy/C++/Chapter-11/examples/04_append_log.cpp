#include <fstream>
#include <iostream>
int main(int argc, char* argv[]) {
    if (argc != 2) { std::cerr << "Usage: append_log <path>\n"; return 1; }
    std::ofstream output{argv[1], std::ios::app};
    if (!output) { std::cerr << "Cannot open log\n"; return 1; }
    output << "INFO,started\n";
    output.close();
    if (!output) { std::cerr << "Write error\n"; return 1; }
    std::cout << "Appended event\n";
}
