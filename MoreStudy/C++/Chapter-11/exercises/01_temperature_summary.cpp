#include <fstream>
#include <print>
#include <string>

// 1행에 정수 1개. 유효 범위: -1000~1000. 공백 행은 오류.
// 입력이 비어 있거나 잘못된 값이 있으면 비정상 종료.
// 출력: Count: N, Min: N, Max: N, Average: N.NN
int main(int argc, char* argv[]) {
    if (argc != 2) return 1;
    std::ifstream input{argv[1]};
    if (!input) return 1;
    std::string line;
    // TODO: std::getline 반복, std::from_chars로 정수 파싱
    // TODO: 개수, 합계, 최솟값, 최댓값 계산
    // TODO: 입력 오류 및 빈 파일 검증 후 결과 출력
    std::println("TODO");
}
