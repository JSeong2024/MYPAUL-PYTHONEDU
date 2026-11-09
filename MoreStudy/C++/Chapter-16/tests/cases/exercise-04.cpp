int main() {
    if (!valid_package_name("Sensor-2")) return 1;
    if (valid_package_name("")) return 2;
    if (valid_package_name("bad name")) return 3;
    if (valid_package_name("name_123")) return 4;
    return 0;
}
