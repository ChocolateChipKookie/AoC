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
	for (std::string l; std::getline(is, l); ) { input_vec.push_back(l); }

	std::vector<std::pair<char, char>> parsed_input;
#if 0
	std::set<char> possible_states;

	for (const std::string& s : input_vec)
	{
		parsed_input.emplace_back(s[5], s[36]);
		possible_states.emplace(s[5]);
		possible_states.emplace(s[36]);
	}

	std::string res;
	
	std::set<char> firsts;
	while(!possible_states.empty())
	{
		for (char s : possible_states)
		{
			bool isFirst = true;
			for (std::pair<char, char> p2 : parsed_input)
			{
				if (s == p2.second)
				{
					isFirst = false;
				}
			}
			if (isFirst)
			{
				firsts.emplace(s);
			}
		}
		char t = *firsts.begin();
		res += t;
		firsts.clear();
		possible_states.erase(possible_states.find(t));

		std::vector<int> to_delete;

		for(unsigned i = 0 ; i < parsed_input.size(); ++i )
		{
			if (parsed_input[i].first == t) to_delete.emplace_back(i);
		}
		
		for (int  i = to_delete.size() - 1; i >= 0 ; --i)
		{
			parsed_input.erase(parsed_input.begin() + to_delete[i]);
		}

		to_delete.clear();

	}

	std::cout << res;

#else

	std::set<char> possible_states;

	for (const std::string& s : input_vec)
	{
		parsed_input.emplace_back(s[5], s[36]);
		possible_states.emplace(s[5]);
		possible_states.emplace(s[36]);
	}

	std::string res;

	std::set<char> firsts;

	bool running = true;
	//na kojem radi i koliko je jos ostalo
	std::vector<std::pair<char, int>> workers(2, {'1', -1});
	int second = -1;
	while (!possible_states.empty() || running)
	{
		running = false;
		for (auto& worker : workers)
		{
			if (worker.second > 0) running = true;
			if (--worker.second == 0)
			{
				res += worker.first;

				std::vector<int> to_delete;

				for (unsigned i = 0; i < parsed_input.size(); ++i)
				{
					if (parsed_input[i].first == worker.first) to_delete.emplace_back(i);
				}

				for (int i = to_delete.size() - 1; i >= 0; --i)
				{
					parsed_input.erase(parsed_input.begin() + to_delete[i]);
				}

				to_delete.clear();

			}
		}

		for (char s : possible_states)
		{
			bool isFirst = true;
			for (std::pair<char, char> p2 : parsed_input)
			{
				if (s == p2.second)
				{
					isFirst = false;
				}
			}
			if (isFirst)
			{
				firsts.emplace(s);
			}
		}

		std::vector<int> to_erase;
		for (int k = 0; k < static_cast<int>(firsts.size()); ++k)
		{
			for(unsigned i = 0; i < workers.size(); ++i)
			{
				if (workers[i].second <= 0)
				{

					char x = *std::next(firsts.begin(), k);
					//staviti 60
					workers[i] = {x, 1 + 60 + x - 'A'};
					to_erase.emplace_back(x);
					break;
				}
			}
		}

		for(int i : to_erase)
		{
			possible_states.erase(possible_states.find(i));
		}
		
		firsts.clear();
		second++;
	}
	std::cout << --second;
#endif
}
