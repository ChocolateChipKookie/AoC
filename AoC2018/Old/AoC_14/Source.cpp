#include <string>
#include <iostream>

int main(){
	const unsigned input = 236021;
	std::string values{ "37" };
	for(unsigned first{ 0 }, second{ 1 }; !(values.size() > 10 && values.substr(values.size() - 10).find(std::to_string(input)) != std::string::npos); values += std::to_string(values[first] + values[second] - 2 * '0')){
		first = (first + 1 + values[first] - '0') % values.size();
		second = (second + 1 + values[second] - '0') % values.size();
	}
	if(input < values.size() + 10)
		std::cout << "Prvi: " << values.substr(input, 10) << '\n';
	std::cout << "Drugi: " << values.find(std::to_string(input)) << '\n';
}
