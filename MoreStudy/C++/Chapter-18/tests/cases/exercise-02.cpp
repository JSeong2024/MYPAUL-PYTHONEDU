#include <stdexcept>
void check(bool v) { if (!v) throw std::runtime_error("parser error"); }
int main() {
 auto a = parse_reading("READ pump-01 1000");
 check(a && a->device == "pump-01" && a->value == 1000);
 auto b = parse_reading("READ Z_9 0");
 check(b && b->value == 0);
 check(!parse_reading("READ x 1001"));
 check(!parse_reading("READ x -1"));
 check(!parse_reading("READ x 5x"));
 check(!parse_reading("READ x 5 "));
 check(!parse_reading("READ  10"));
 check(!parse_reading("READ A! 42"));
 check(!parse_reading("READ aaaaaaaaaaaaaaaaa 1"));
 check(!parse_reading("READ x +1"));
 check(!parse_reading("RExD x 10"));
}
