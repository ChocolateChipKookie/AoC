#include <string>
#include <vector>
#include <fstream>
#include <iostream>


int main(int argc, char* argv[])
{
	std::ifstream is("input.txt");
	std::vector<std::string> input_vec; // { std::istream_iterator<std::string>(is), std::istream_iterator<std::string>()};
	for (std::string l; std::getline(is, l); ) { input_vec.push_back(l); }

	for(auto& name : input_vec)
	{
		bool a{ false }, e{ false }, i{ false }, o{ false }, u{ false };

		for(int j = 0; name[j] != '-'; ++j)
		{
			if (name[j] == 'a' || name[j] == 'A') a = true;
			if (name[j] == 'e' || name[j] == 'E') e = true;
			if (name[j] == 'i' || name[j] == 'I') i = true;
			if (name[j] == 'o' || name[j] == 'O') o = true;
			if (name[j] == 'u' || name[j] == 'U') u = true;
		}
		if (a&&e&&i&&o&&u)
		{
			std::cout << name << '\n';
		}
	}
	while (true);
}
