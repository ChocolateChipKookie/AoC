#include <iostream>
#include <string>
#include <vector>

int main(int argc, char* argv[])
{
	std::string input;

#if 0
	int threes{ 0 };
	int doubles{ 0 };

	while(true)
	{
		int arr[26]{ 0 };
		std::cin >> input;
		if (input == ".") break;
		for(char c : input)
		{
			arr[c - 'a']++;
		}
		for (int i : arr)
		{
			if (i == 2)
			{
				doubles++;
				break;
			}
		}
		for (int i : arr)
		{
			if (i == 3)
			{
				threes++;
				break;
			}
		}
		input = "";
	}
	std::cout << threes * doubles;
	return 0;
#else
	int threes{ 0 };
	int doubles{ 0 };
	std::vector<std::string> inputs;
	while (true)
	{
		std::cin >> input;
		if (input == ".")break;
		inputs.push_back(input);
	}

	for (unsigned int j = 0; j < inputs.size(); ++j)
	{
		std::string& first = inputs.at(j);
		for (unsigned int k = j + 1; k < inputs.size(); ++k)
		{
			std::string& second = inputs.at(k);
			unsigned difference = 0;
			for(unsigned int i = 0; i < first.length(); ++i)
			{
				if (first[i] != second[i]) difference++;
			}
			if(difference == 1)
			{
				for (unsigned int i = 0; i < first.length(); ++i)
				{
					if (first[i] == second[i]) std::cout << first[i];
				}
				return 0;
			}
		}
	}

#endif
}
