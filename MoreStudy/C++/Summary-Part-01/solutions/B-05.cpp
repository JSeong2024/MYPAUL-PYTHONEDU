#include <iostream>
#include <string>

class LibraryBook {
public:
    LibraryBook(std::string title, int total)
        : title_(title), total_(total), available_(total) {}

    bool borrow() {
        if (available_ == 0) return false;
        --available_;
        return true;
    }

    bool give_back() {
        if (available_ == total_) return false;
        ++available_;
        return true;
    }

    int available() const { return available_; }

private:
    std::string title_;
    int total_;
    int available_;
};

int main() {
    std::string title;
    int total = 0;
    int count = 0;
    if (!(std::cin >> title >> total >> count) || total < 0 || total > 1000 ||
        count < 0 || count > 1000) {
        std::cout << "INVALID\n";
        return 0;
    }

    LibraryBook book(title, total);
    for (int i = 0; i < count; ++i) {
        std::string command;
        if (!(std::cin >> command)) {
            std::cout << "INVALID\n";
            return 0;
        }
        const bool ok = command == "BORROW" ? book.borrow()
                        : command == "RETURN" && book.give_back();
        std::cout << (ok ? "OK " : "FAIL ") << book.available() << '\n';
    }
}
