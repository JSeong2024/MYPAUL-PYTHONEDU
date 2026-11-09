#include <string_view>
int main() {
#ifdef CH16_DIAGNOSTICS
    return feature_label() == "diagnostics-on" ? 0 : 1;
#else
    return feature_label() == "diagnostics-off" ? 0 : 2;
#endif
}
