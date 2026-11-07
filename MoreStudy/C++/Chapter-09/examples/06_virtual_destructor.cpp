#include <memory>
#include <print>

class Connection {
public:
    virtual ~Connection() { std::println("Connection closed"); }
    virtual void send() const = 0;
};

class SerialConnection final : public Connection {
public:
    ~SerialConnection() override { std::println("Serial resource released"); }
    void send() const override { std::println("Sending packet"); }
};

int main() {
    std::unique_ptr<Connection> connection =
        std::make_unique<SerialConnection>();
    connection->send();
}  // 파생 클래스 소멸자부터 순서대로 호출
