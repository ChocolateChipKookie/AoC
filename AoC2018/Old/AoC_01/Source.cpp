#include <fstream>
#include <string>
#include <iostream>
#include <vector>

bool contains(std::vector<int>& vec, int n)
{
	for (int i : vec) if (i == n)return true;
	return false;
}

int main(int argc, char* argv[])
{

	int counter = 0;
	std::ifstream input("input.txt");
	std::string str;
#if 0
	while(!input.eof())
	{
		std::getline(input, str);
		if(str[0] == '+')
		{
			counter+=std::stoi(str.substr(1));
		}
		else
		{
			counter -= std::stoi(str.substr(1));
		}
	}

	std::cout << couter;
#else

	std::vector<int> contained;
	std::vector<int> inputs;
	contained.push_back(0);
	int i = 0;

	while (!input.eof())
	{
		std::getline(input, str);
		if (str.size() == 0) {
			std::cout << str;
		}
		if (str[0] == '+')
		{
			inputs.push_back(std::stoi(str.substr(1)));
		}
		else
		{
			inputs.push_back(-std::stoi(str.substr(1)));
		}
		i++;
	}

	i = 0;
	while (true)
	{
		counter += inputs[i++];
		i %= inputs.size();
		if (contains(contained, counter))
		{
			std::cout << counter;
			break;
		}
		else
		{
			contained.push_back(counter);
		}
	}

	return 0;
#endif
}


