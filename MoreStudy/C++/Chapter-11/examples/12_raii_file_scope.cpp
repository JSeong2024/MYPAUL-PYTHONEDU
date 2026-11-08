#include <fstream>
#include <iostream>
#include <string>
int main(int argc, char* argv[]) {
    if (argc != 2) { std::cerr << "Usage: raii_file_scope <path>\n"; return 1; }
    { std::ofstream output{argv[1]};
      if (!output) { return 1; }
      output << "status=ready\n";
      output.close();
      if (!output) { return 1; }
    }
    std::ifstream input{argv[1]};
    std::string line;
    if (!std::getline(input,line)) { return 1; }
    std::cout << line << '\n';
}
