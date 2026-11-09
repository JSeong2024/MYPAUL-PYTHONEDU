#define CH17_LIBRARY_ONLY
#include CH17_SOURCE_PATH
#include <array>
#include <stdexcept>
struct Fake final: ReadingSource {
 std::array<std::optional<int>,5> values{70,80,std::nullopt,91,79};
 std::size_t index{};
 std::optional<int> next() override {
  if(index>=values.size())throw std::runtime_error("overread");
  return values[index++];
 }
};
int main(){
 Fake fake;
 if(count_alerts(fake,4,80)!=2 || fake.index!=4)throw std::runtime_error("count");
 Fake none;
 if(count_alerts(none,0,80)!=0 || none.index!=0)throw std::runtime_error("zero reads");
 Fake all;
 if(count_alerts(all,5,70)!=4)throw std::runtime_error("lower threshold");
}
