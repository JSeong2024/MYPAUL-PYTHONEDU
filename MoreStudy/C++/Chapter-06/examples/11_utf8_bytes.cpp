#include <print>
#include <string>

int main() {
    // UTF-8: 'A' 1바이트 + '한' 3바이트. 소스 파일 인코딩에 의존하지 않음.
    const std::string text{"A\xED\x95\x9C"};
    std::println("Bytes: {}", text.size());
    std::println("First ASCII byte: {}", text.front());
    // size()는 Unicode 문자 수나 사용자에게 보이는 글자 수가 아님.
}
