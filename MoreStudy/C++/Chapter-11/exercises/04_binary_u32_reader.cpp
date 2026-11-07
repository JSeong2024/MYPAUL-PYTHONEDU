#include <cstdint>
#include <fstream>
#include <print>

// CNT1(4 bytes) + count(uint32 Big Endian) + count*uint32(Big Endian)
// count <= 100000. 데이터 부족/초과/잘못된 Magic은 오류.
// 출력: Count: N, Sum: N
int main(int argc, char* argv[]) {
    if (argc != 2) return 1;
    std::ifstream input{argv[1], std::ios::binary};
    if (!input) return 1;
    // TODO: Magic, Count, Values 순서로 읽고 길이를 검증
    // TODO: uint64_t로 합산하고 출력
    std::println("TODO");
}
