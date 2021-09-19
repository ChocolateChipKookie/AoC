#include <string>
#include <iterator>
#include <iostream>
#include <vector>
#include <algorithm>
#include <map>
#include <numeric>
#include <fstream>
#include <sstream>
#include <set>

std::vector<int> regs(4, 0);

int addr(int a, int b)
{
	return regs[a] + regs[b];
}

int addi(int a, int b)
{
	return regs[a] + b;
}

int mulr(int a, int b)
{
	return regs[a] * regs[b];
}

int muli(int a, int b)
{
	return regs[a] * b;
}

int banr(int a, int b)
{
	return regs[a] & regs[b];
}

int bani(int a, int b)
{
	return regs[a] & b;
}

int borr(int a, int b)
{
	return regs[a] | regs[b];
}

int bori(int a, int b)
{
	return regs[a] | b;
}

int setr(int a, int b)
{
	return regs[a];
}

int seti(int a, int b)
{
	return a;
}

int gtir(int a, int b)
{
	return a > regs[b];
}

int gtri(int a, int b)
{
	return regs[a] > b;
}

int gtrr(int a, int b)
{
	return regs[a] > regs[b];
}

int eqir(int a, int b)
{
	return a == regs[b];
}

int quri(int a, int b)
{
	return regs[a] == b;
}

int eqrr(int a, int b)
{
	return regs[a] == regs[b];
}

std::vector<int> parse(std::string& s)
{
	std::istringstream iss(s);
	std::vector<int> results((std::istream_iterator<int>(iss)), std::istream_iterator<int>());
	return	results;
}

void first()
{
	std::ifstream is("input1.txt");
	std::vector<std::string> input_vec; // { std::istream_iterator<std::string>(is), std::istream_iterator<std::string>()};
	for (std::string l; std::getline(is, l); ) { input_vec.push_back(l); }

	std::string input;
	std::getline(std::ifstream{ "input.txt" }, input);

	std::vector<std::tuple<std::vector<int>, std::vector<int>, std::vector<int>>> triplets;

	for (unsigned i = 0; i < input_vec.size() / 4; ++i)
	{
		std::string start = input_vec[i * 4 + 0].substr(0, input_vec[i * 4 + 0].size() - 1).substr(input_vec[i * 4 + 0].find('[') + 1);
		std::string command = input_vec[i * 4 + 1];
		std::string result = input_vec[i * 4 + 2].substr(0, input_vec[i * 4 + 2].size() - 1).substr(input_vec[i * 4 + 2].find('[') + 1);

		triplets.emplace_back(parse(start), parse(command), parse(result));
	}

	int real_deal{ 0 };

	std::set<std::string> tmp;

	for (auto& t : triplets)
	{
		regs = std::get<0>(t);
		auto& command = std::get<1>(t);
		auto& result = std::get<2>(t);

		int counter = 0;
		int a{ command[1] }, b{ command[2] }, c{ command[3] };
		if (result[c] == addr(a, b)) counter++;
		if (result[c] == addi(a, b)) counter++;
		if (result[c] == mulr(a, b)) counter++;
		if (result[c] == muli(a, b)) counter++;
		if (result[c] == banr(a, b)) counter++;
		if (result[c] == bani(a, b)) counter++;
		if (result[c] == borr(a, b)) counter++;
		if (result[c] == bori(a, b)) counter++;
		if (result[c] == setr(a, b)) counter++;
		if (result[c] == seti(a, b)) counter++;
		if (result[c] == gtir(a, b)) counter++;
		if (result[c] == gtri(a, b)) counter++;
		if (result[c] == gtrr(a, b)) counter++;
		if (result[c] == eqir(a, b)) counter++;
		if (result[c] == quri(a, b)) counter++;
		if (result[c] == eqrr(a, b)) counter++;
		if (counter > 2) real_deal++;
	}

	for (auto& t : tmp) {
		std::cout << t << '\n';
	}

	std::cout << "Prvi: " << real_deal << '\n';
}

void second()
{
	std::ifstream is("input2.txt");
	std::vector<std::string> input_vec; // { std::istream_iterator<std::string>(is), std::istream_iterator<std::string>()};
	for (std::string l; std::getline(is, l); ) { input_vec.push_back(l); }
	regs = std::vector<int>(4, 0);

	std::vector<std::vector<int>> commands;

	for (auto& s : input_vec){
		commands.emplace_back(parse(s));
	}

	for (auto& t : commands)
	{
		switch(t[0])
		{
		case 0:
			regs[t[3]] = quri(t[1], t[2]);
			break;
		case 1:
			regs[t[3]] = bori(t[1], t[2]);
			break;
		case 2:
			regs[t[3]] = addi(t[1], t[2]);
			break;
		case 3:
			regs[t[3]] = bani(t[1], t[2]);
			break;
		case 4:
			regs[t[3]] = seti(t[1], t[2]);
			break;
		case 5:
			regs[t[3]] = eqrr(t[1], t[2]);
			break;
		case 6:
			regs[t[3]] = addr(t[1], t[2]);
			break;
		case 7:
			regs[t[3]] = gtri(t[1], t[2]);
			break;
		case 8:
			regs[t[3]] = borr(t[1], t[2]);
			break;
		case 9:
			regs[t[3]] = gtir(t[1], t[2]);
			break;
		case 10:
			regs[t[3]] = setr(t[1], t[2]);
			break;
		case 11:
			regs[t[3]] = eqir(t[1], t[2]);
			break;
		case 12:
			regs[t[3]] = mulr(t[1], t[2]);
			break;
		case 13:
			regs[t[3]] = muli(t[1], t[2]);
			break;
		case 14:
			regs[t[3]] = gtrr(t[1], t[2]);
			break;
		case 15:
			regs[t[3]] = banr(t[1], t[2]);
			break;
		}
	}

	std::cout << "Drugi: " << regs[0] << '\n';
}

int main()
{
	first();
	second();
	while (true);

}