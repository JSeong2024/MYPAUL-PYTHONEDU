#include <cstddef>
#include <optional>
struct ReadingSource {
    virtual ~ReadingSource() = default;
    virtual std::optional<int> next() = 0;
};
std::size_t count_alerts(ReadingSource& source, std::size_t max_samples, int threshold) {
    std::size_t alerts=0;
    for(std::size_t i=0;i<max_samples;++i) {
        const auto reading=source.next();
        if(reading && *reading>=threshold) ++alerts;
    }
    return alerts;
}
#ifndef CH17_LIBRARY_ONLY
#include <iostream>
struct Fake final: ReadingSource {std::optional<int> next() override{return 90;}};
int main(){Fake source;std::cout << "Alerts: " << count_alerts(source,3,80) << '\n';}
#endif
