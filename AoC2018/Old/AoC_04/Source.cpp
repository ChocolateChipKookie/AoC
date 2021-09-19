#include <string>
#include <iterator>
#include <iostream>
#include <vector>
#include <algorithm>
#include <map>
#include <numeric>
#include <fstream>

using tuple = std::tuple<int, int, int, int>;


int main()
{
	std::ifstream is("input.txt");
	std::vector<std::string> inputs; // { std::istream_iterator<std::string>(is), std::istream_iterator<std::string>()};
	for (std::string l; std::getline(is, l); ) { inputs.push_back(l); }

	std::sort(inputs.begin(), inputs.end());
	std::map<int, int[60]> map;
	int current_id;
	int minute{0};
	for(const std::string& input : inputs){
		unsigned i;
		if ((i = input.find('#')) != std::string::npos){
			current_id = std::stoi(input.substr(i + 1));
		}
		else if (input.find("falls") != std::string::npos){
			minute = std::stoi(input.substr(15, 2));
		}
		else{
			if(!map.count(current_id)){
				std::fill(std::begin(map[current_id]), std::end(map[current_id]), 0);
			}
			for (unsigned j = minute, k = std::stoi(input.substr(15, 2)); j < k; ++j){
				map[current_id][j]++;
			}
		}
	}
	//id, minute, maxminute, value
	std::vector<tuple> values;
	values.reserve(map.size());
	for (auto& it : map)
	{
		int *max_ele{ std::max_element(std::begin(it.second), std::end(it.second)) };
		values.emplace_back(it.first, 
			std::distance(std::begin(it.second), max_ele),
			*max_ele,
			std::accumulate(std::begin(it.second), std::end(it.second), 0));
	}
	
	tuple rj1 = *std::max_element(values.begin(), values.end(), 
		[](tuple t1, tuple t2) {return std::get<3>(t1) < std::get<3>(t2); });
	tuple rj2 = *std::max_element(values.begin(), values.end(),
		[](tuple t1, tuple t2) {return std::get<2>(t1) < std::get<2>(t2); });

	std::cout << "1: " << std::get<0>(rj1)*std::get<1>(rj1) << "\n2: " << std::get<0>(rj2)*std::get<1>(rj2);
	int i;
	std::cin >> i;
	return 0;
}
