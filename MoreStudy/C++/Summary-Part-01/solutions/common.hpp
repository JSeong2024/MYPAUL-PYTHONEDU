#ifndef SUMMARY_PART_01_COMMON_HPP
#define SUMMARY_PART_01_COMMON_HPP
#include <charconv>
#include <cctype>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <limits>
#include <optional>
#include <string>
#include <string_view>
#include <system_error>
#include <vector>
namespace summary {
inline void strip_cr(std::string& s) { if (!s.empty() && s.back() == '\r') s.pop_back(); }
inline std::string trim(std::string_view s) {
    while (!s.empty() && std::isspace(static_cast<unsigned char>(s.front()))) s.remove_prefix(1);
    while (!s.empty() && std::isspace(static_cast<unsigned char>(s.back()))) s.remove_suffix(1);
    return std::string(s);
}
inline std::optional<std::int64_t> number(std::string_view s) {
    if (s.empty()) return std::nullopt;
    std::int64_t v=0;
    auto [p,ec]=std::from_chars(s.data(),s.data()+s.size(),v);
    if (ec!=std::errc{} || p!=s.data()+s.size()) return std::nullopt;
    return v;
}
inline std::vector<std::string> split(std::string_view s) {
    std::vector<std::string> result;
    std::size_t pos=0;
    while (true) {
        const auto comma=s.find(',',pos);
        result.emplace_back(s.substr(pos,comma==std::string_view::npos?comma:comma-pos));
        if (comma==std::string_view::npos) break;
        pos=comma+1;
    }
    return result;
}
inline bool safe_write(const std::filesystem::path& target, const std::string& body, std::string& error) {
    const auto temp=std::filesystem::path(target.string()+".tmp");
    {
        std::ofstream out(temp,std::ios::binary|std::ios::trunc);
        if (!out) {error="cannot open "+temp.string();return false;}
        out<<body;
        out.flush();
        if (!out) {error="cannot write "+temp.string();return false;}
        out.close();
        if (!out) {error="cannot close "+temp.string();return false;}
    }
    std::error_code ec;
    std::filesystem::rename(temp,target,ec);
    if (!ec) return true;
    // Fallback for platforms that do not permit rename over an existing file.
    // This is NOT an atomic replacement; refer to R-01_ERROR_CODES.md.
    std::error_code check;
    if (!std::filesystem::is_regular_file(target,check) || check) {
        error="cannot replace "+target.string()+": "+ec.message();return false;
    }
    const auto backup=std::filesystem::path(target.string()+".bak");
    if (std::filesystem::exists(backup,check) || check) {
        error="backup already exists or unavailable: "+backup.string();return false;
    }
    std::filesystem::rename(target,backup,ec);
    if (ec) {error="backup failed: "+ec.message();return false;}
    std::filesystem::rename(temp,target,ec);
    if (ec) {
        std::error_code restoration;
        std::filesystem::rename(backup,target,restoration);
        error="replacement failed: "+ec.message();
        if (restoration) error+="; restoration failed: "+restoration.message();
        return false;
    }
    std::filesystem::remove(backup,check);
    if (check) {error="output updated but backup removal failed: "+check.message();return false;}
    return true;
}
}
#endif
