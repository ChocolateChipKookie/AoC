#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <ctype.h>

int main()
{
	std::string input;
	std::getline(std::ifstream{ "input.txt" }, input);
	input = '#' + input;
#if 0
	//1. dio
	for (unsigned i = 0; i < input.size() - 1; ++i)
		if (std::abs(input[i] - input[i + 1]) == 32) { input.erase(i, 2); i -= 2; }

	std::cout << input.size() - 1;
#else
	//2. dio
	std::vector<unsigned> solutions;
	for (char i = 'a'; i <= 'z'; ++i)
	{
		std::string in = input;
		for (unsigned j = 0; j < in.size() - 1; ++j)
			if (tolower(in[j]) == i) { in.erase(j, 1); j -= 2; }
			else if (std::abs(in[j] - in[j + 1]) == 32) { in.erase(j, 2); j -= 2; }
		
		solutions.emplace_back(in.size() - 1);
	}
	std::cout << *std::min_element(solutions.begin(), solutions.end());
#endif
	return 0;
}
