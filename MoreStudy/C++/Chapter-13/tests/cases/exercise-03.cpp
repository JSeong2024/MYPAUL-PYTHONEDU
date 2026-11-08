#include <cassert>
#include <string>
#include <vector>
#include CH13_SOURCE_PATH
int main() {
    const std::vector<Device> source{{"Z",80,true},{"B",95,false},
                                     {"A",90,true},{"C",79,true},{"D",80,true}};
    const auto result=selected_devices(source,80);
    assert(result.size()==3);
    assert(result[0].id=="A" && result[1].id=="D" && result[2].id=="Z");
    assert(source[0].id=="Z");
    assert(selected_devices(source,101).empty());
    assert(selected_devices({},0).empty());
}
