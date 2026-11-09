#include "quality_gate/batch.hpp"
#include <array>
#include <iostream>
int main() {
 const std::array input{quality_gate::Reading{"D2",20,true},quality_gate::Reading{"D1",10,true},
                        quality_gate::Reading{"D2",50,true},quality_gate::Reading{"D3",-3,false}};
 const auto rows=quality_gate::summarize(input);
 std::cout<<"Devices: "<<rows.size()<<'\n';
 for(const auto& row:rows)std::cout<<row.device<<','<<row.count<<','<<row.total<<'\n';
}
