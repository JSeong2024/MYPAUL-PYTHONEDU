#include <filesystem>
#include <fstream>
#include <iostream>
#include <system_error>
int main(int argc,char* argv[]) {
    if (argc != 2) { std::cerr << "Usage: rename_save <path>\n"; return 1; }
    const std::filesystem::path target{argv[1]};
    const std::filesystem::path temporary = target.string() + ".tmp";
    if (std::filesystem::exists(temporary)) { std::cerr << "Temporary file exists\n"; return 1; }
    { std::ofstream file{temporary};
      if (!file) { return 1; }
      file << "reading=24\n";
      file.close();
      if (!file) { std::filesystem::remove(temporary); return 1; }
    }
    std::error_code ec;
    std::filesystem::rename(temporary,target,ec);
    if (ec) { std::filesystem::remove(temporary); std::cerr << "Rename failed\n"; return 1; }
    std::cout << "Saved report\n";
}
