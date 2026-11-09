#include "quality_gate/batch.hpp"
#include <map>
#include <stdexcept>
#include <utility>
namespace quality_gate {
std::vector<Summary> summarize(std::span<const Reading> readings) {
 std::map<std::string,Summary> groups;
 for(const auto& r:readings) {
  if(!r.valid) continue;
  if(r.device.empty() || r.value<0 || r.value>100) throw std::invalid_argument("invalid reading");
  auto [it,inserted]=groups.try_emplace(r.device,Summary{r.device,0,0,r.value,r.value});
  (void)inserted;
  auto& item=it->second;
  ++item.count; item.total+=r.value;
  if(r.value<item.minimum)item.minimum=r.value;
  if(r.value>item.maximum)item.maximum=r.value;
 }
 std::vector<Summary> result;result.reserve(groups.size());
 for(auto& [key,item]:groups) { (void)key;result.push_back(std::move(item)); }
 return result;
}
}
