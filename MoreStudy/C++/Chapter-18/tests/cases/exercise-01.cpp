#include <stdexcept>
#include <string>
void check(bool v) {if (!v) throw std::runtime_error("frame decoder error");}
int main() {
 check(decode(std::string{"\0\0\0\4PING",8}).value_or("") == "PING");
 check(decode(std::string(4,'\0')).has_value());
 check(decode(std::string{"\0\0\0\2\0Z",6}).value_or("x") == std::string("\0Z",2));
 check(!decode("abc"));
 check(!decode(std::string{"\0\0\0\4PIN",7}));
 check(!decode(std::string{"\0\0\0\4PINGX",9}));
 check(!decode(std::string{"\0\0\x10\x01",4}));
}
