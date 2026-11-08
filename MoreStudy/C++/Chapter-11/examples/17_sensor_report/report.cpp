#include "report.hpp"
#include <charconv>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <limits>
#include <sstream>
#include <locale>
#include <string>
#include <system_error>
std::optional<SensorReport> build_report(const std::filesystem::path& input_path) {
 std::ifstream input{input_path};if(!input){return std::nullopt;}
 std::string line;SensorReport report{};double total{};
 while(std::getline(input,line)){
  const auto comma=line.find(',');
  if(comma==std::string::npos||comma==0||comma+1==line.size()||line.find(',',comma+1)!=std::string::npos){return std::nullopt;}
  const std::string device=line.substr(0,comma);const std::string text=line.substr(comma+1);
  // ASCII decimal values use the stream's classic locale to avoid machine-specific decimal formats.
  std::istringstream parser{text};parser.imbue(std::locale::classic());
  double value{};char rest{};
  if(!(parser>>value)||(parser>>rest)||!std::isfinite(value)||value<-100.0||value>100.0){return std::nullopt;}
  if(report.samples==0){report.minimum=value;report.maximum=value;}
  if(value<report.minimum)report.minimum=value;
  if(value>report.maximum)report.maximum=value;
  ++report.counts[device];++report.samples;total+=value;
 }
 if(input.bad()||report.samples==0){return std::nullopt;}
 report.average=total/static_cast<double>(report.samples);
 return report;
}
bool write_report(const std::filesystem::path& output_path,const SensorReport& report){
 std::ofstream output{output_path};if(!output){return false;}
 output.imbue(std::locale::classic());
 output<<std::fixed<<std::setprecision(2)
  <<"Samples: "<<report.samples<<'\n'<<"Devices: "<<report.counts.size()<<'\n'
  <<"Min: "<<report.minimum<<'\n'<<"Max: "<<report.maximum<<'\n'
  <<"Average: "<<report.average<<'\n';
 for(const auto& [name,count]:report.counts){output<<name<<": "<<count<<'\n';}
 output.close();return static_cast<bool>(output);
}
