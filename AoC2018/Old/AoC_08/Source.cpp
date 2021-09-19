#include <string>
#include <iterator>
#include <iostream>
#include <vector>
#include <numeric>
#include <fstream>

struct node
{
	std::vector<node> subnodes;
	std::vector<unsigned> values;
};

int task_1(node& n)
{
	int result = std::accumulate(n.values.begin(), n.values.end(), 0);
	for(node& sn : n.subnodes)result += task_1(sn);
	return result;
}

int task_2(node& n)
{
	if(n.subnodes.empty())return std::accumulate(n.values.begin(), n.values.end(), 0);

	int result{ 0 };
	for(int i = 0; i < n.values.size(); ++i)
		if(n.values[i] <= n.subnodes.size())
			result += task_2(n.subnodes[n.values[i] - 1]);
	return result;
}

node recursive_parse(std::vector<int>& inputs, int node_start)
{
	node n;
	if (inputs[node_start] != 0) {
		for (int i = 0; i < inputs[node_start]; ++i)
			n.subnodes.emplace_back(recursive_parse(inputs, node_start + 2));
	}
	for (int i = 0; i < inputs[node_start + 1]; ++i)
		n.values.emplace_back(inputs[node_start + 2 + i]);

	inputs.erase(inputs.begin() + node_start, inputs.begin() + node_start + 2 + inputs[node_start + 1]);
	return n;
}

int main()
{
	std::ifstream is("input.txt");
	std::vector<int> input_vec { std::istream_iterator<int>(is), std::istream_iterator<int>()};
	node n = recursive_parse(input_vec, 0);

	std::cout << "1.Zadatak:" << task_1(n) << '\n';
	std::cout << "2.Zadatak:" << task_2(n) << '\n';

	return 0;
}