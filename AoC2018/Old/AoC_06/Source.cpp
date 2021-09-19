#include <string>
#include <iterator>
#include <iostream>
#include <vector>
#include <algorithm>
#include <map>
#include <numeric>
#include <fstream>
#include <set>

int find_closest(std::vector<std::pair<int, int>>& positions, std::pair<int, int>&& pos){
	int res{0}, tmp, min_distance{ 10000 };
	for(unsigned i = 0; i < positions.size(); ++i){
		if ((tmp = std::abs(positions[i].first - pos.first) + std::abs(positions[i].second - pos.second)) < min_distance) {
			min_distance = tmp; res = i;
		}
		else if (tmp == min_distance)res = -1;
	}
	return res;
}

int main(){
	std::ifstream is("input.txt");
	std::vector<std::pair<int, int>> positions;
	std::pair<int, int> helper, virtual_size{ 0,0 };
	char c;

	while (!is.eof()){
		is >> helper.first >> c >> helper.second;
		virtual_size = {std::max(virtual_size.first, helper.first), std::max(virtual_size.second, helper.second)};
		positions.emplace_back(helper);
	}

	//1. Dio
	std::vector<std::vector<int>> closest_cords(virtual_size.first + 1);
	for(int i = 0; i <= virtual_size.first ; ++i){
		closest_cords.emplace_back(std::vector<int>(virtual_size.second + 1));
		for (int j = 0; j < virtual_size.second; ++j)
			closest_cords[i].emplace_back(find_closest(positions, std::pair<int, int>(i, j)));
	}

	std::set<int> edges;
	edges.emplace(-1);
	for (int i = 0, k = std::max(virtual_size.first, virtual_size.first); i <= k; ++i){
		if(i < virtual_size.first){
			edges.emplace(closest_cords[i][0]);
			edges.emplace(closest_cords[i][virtual_size.second - 1]);
		}
		if(i < virtual_size.second){
			edges.emplace(closest_cords[0][i]);
			edges.emplace(closest_cords[virtual_size.first - 1][i]);
		}
	}

	std::vector<int> counter(positions.size(), 0);
	for (int i = 0; i < virtual_size.first; ++i)
		for (int j = 0; j < virtual_size.second; ++j)
			if (edges.find(closest_cords[i][j]) == edges.end())
				counter[closest_cords[i][j]]++;
	std::cout << *std::max_element(counter.begin(), counter.end());

	//2.
	int res { 0 };
	for (int i = 0; i < virtual_size.first; ++i)
		for (int j = 0, sum{ 0 }; j < virtual_size.second; ++j, sum  = 0) {
			for (auto& p : positions)
				sum += std::abs(p.first - i) + std::abs(p.second - j);
			if (sum < 10000)res++;
		}

	std::cout << res;
	return 0;
}
