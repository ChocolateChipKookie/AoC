#include <string>
#include <iterator>
#include <iostream>
#include <vector>
#include <sstream>

struct piece
{
	int id, x, y, width, height;
};

int main(int argc, char* argv[])
{
	std::vector<std::string> v;
	std::vector<piece> pieces;
	std::string in;
	while(true)
	{
		std::cin >> in;
		if (in == ".")break;
		v.emplace_back(in);
	}

	int maxX{ 0 }, maxY{0};

	for(unsigned i = 0; i < v.size() / 4; ++i)
	{
		piece tmp;
		tmp.id = std::stoi(v[i*4].substr(1));
		int j = v[i * 4 + 2].find(',');
		tmp.x = std::stoi(v[i * 4 + 2].substr(0, j));
		std::string help = v[i * 4 + 2].substr(j + 1);
		tmp.y = std::stoi(help.substr(0, help.length() - 1));

		j = v[i * 4 + 3].find('x');
		tmp.width = std::stoi(v[i * 4 + 3].substr(0, j));
		tmp.height = std::stoi(v[i * 4 + 3].substr(j + 1));
		pieces.emplace_back(tmp);

		if (tmp.x + tmp.width > maxX)maxX = tmp.x + tmp.width;
		if (tmp.y + tmp.height > maxY)maxY = tmp.y + tmp.height;
	}

	int* arr = new int[maxX * maxY]{0};

	for(piece p : pieces)
	{
		for(int x = 0; x < p.width; ++x)
		{
			for (int y = 0; y < p.height; ++y)
			{
				arr[(y + p.y)*maxY + x + p.x]++;
			}
		}
	}

#if 0
	//1
	int counter = 0;
	for(int i = 0; i < maxX*maxY; ++i)
	{
		if (arr[i] > 1)counter++;
	}
	std::cout << counter;
#else
	//2
	for (piece p : pieces)
	{
		bool single{ true };
		for (int x = 0; x < p.width; ++x)
		{
			for (int y = 0; y < p.height; ++y)
			{
				if(arr[(y + p.y)*maxY + x + p.x] != 1)
				{
					single = false;
					break;
				}
			}
		}
		if (single) std::cout << p.id;
	}
#endif
	return 0;
}
