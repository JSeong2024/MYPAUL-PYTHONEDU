#include <stdexcept>
void check(bool v){if(!v)throw std::runtime_error("retry policy error");}
int main() {
 check(should_retry(Failure::timeout,1,3));
 check(should_retry(Failure::unavailable,2,3));
 check(!should_retry(Failure::invalid_request,1,3));
 check(!should_retry(Failure::rejected,1,3));
 check(!should_retry(Failure::timeout,3,3));
 check(!should_retry(Failure::timeout,0,3));
 check(!should_retry(Failure::timeout,1,0));
 check(!should_retry(Failure::timeout,-1,2));
}
