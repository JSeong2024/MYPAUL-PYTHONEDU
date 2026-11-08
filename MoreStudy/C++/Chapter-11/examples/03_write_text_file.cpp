#include <fstream>
#include <iostream>
int main(int argc, char* argv[]) {
    if (argc != 2) { std::cerr << "Usage: write_text_file <path>\n"; return 1; }
    std::ofstream output{argv[1], std::ios::trunc};
    if (!output) { std::cerr << "Cannot create file\n"; return 1; }
    output << "device,temperature\n" << "SENSOR-A,23\n";
    output.close();
    if (!output) { std::cerr << "Write error\n"; return 1; }
    std::cout << "Saved 2 lines\n";
}
