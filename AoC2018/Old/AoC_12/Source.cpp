#include <string>
#include <iterator>
#include <iostream>
#include <vector>
#include <algorithm>
#include <map>
#include <numeric>
#include <fstream>
#include <set>


int main()
{
	std::ifstream is("input.txt");
	std::vector<std::string> input_vec;

	std::string plants;
	std::getline(is, plants);
	plants = plants.substr(plants.find(':') + 2);
	
	for (std::string l; std::getline(is, l); ) { input_vec.push_back(l); }
	input_vec.erase(input_vec.begin());
	
	std::set<std::string> new_plant;

	for (const std::string& s : input_vec){
		if(s.back() == '#'){
			const int pos = s.find(' ');
			new_plant.emplace(s.substr(0, pos));
		}
	}
	const int generations{ 20 };
	std::string pots{ std::string(generations, '.') + plants + std::string(generations, '.') };

	for(unsigned i = 0; i < generations; ++i){
		std::string new_pots(pots.size(), '.');
		for(unsigned j = 2; j < pots.size() - 2; ++j){
			if(new_plant.count(pots.substr(j - 2, 5)))
				new_pots[j] = '#';
		}
		pots = new_pots;
	}

	int result = 0;
	for (int i = 0; i < pots.size(); ++i)
		if (pots[i] == '#')
			result += i - generations;

	std::cout << result << '\n';

	//2.zad
	std::cout << 23 * 50000000000ll + 457;
}
