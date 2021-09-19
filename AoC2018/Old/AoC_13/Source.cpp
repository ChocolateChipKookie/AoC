#include <string>
#include <iterator>
#include <iostream>
#include <vector>
#include <algorithm>
#include <map>
#include <numeric>
#include <fstream>
#include <xmmintrin.h>

struct cart
{
	int x, y;
	int direction;
	int last_intersection{-1};
	bool check{ true };
};

bool sort_carts(cart& c1, cart& c2)
{
	return c1.x + c1.y * 200 < c2.x + c2.y * 200;
}

bool collides(cart& c, std::vector<cart>& carts)
{
	int same{ 0 };

	for(auto& c1 : carts)
	{
		if (!c1.check) continue;
		if(c1.x == c.x && c1.y == c.y)
		{
			++same;
		}
	}
	return same > 1;
}

int main()
{
	std::ifstream is("input.txt");
	std::vector<std::string> input_vec;
	for (std::string l; std::getline(is, l); ) { input_vec.push_back(l); }

	std::string input;
	std::getline(std::ifstream{ "input.txt" }, input);

	std::vector<int> parsed_input;

	std::vector<cart> carts;

	for (int i = 0; i < static_cast<int>(input_vec.size()); ++i)
	{
		unsigned pos;
		while ((pos = input_vec[i].find_first_of("v^<>")) != std::string::npos)
		{
			int direction = 0;
			switch (input_vec[i][pos])
			{
			case '>':
				direction = 0;
				break;
			case 'v':
				direction = 1;
				break;
			case '<':
				direction = 2;
				break;
			case '^':
				direction = 3;
			}
			if(input_vec[i][pos - 1] == '-' || input_vec[i][pos + 1] == '-')
			{
				input_vec[i][pos] = '-';
			}
			else
			{
				input_vec[i][pos] = '|';
			}
			carts.push_back({static_cast<int>(pos), static_cast<int>(i), direction});
		}
	}


	while(true)
	{
		std::sort(carts.begin(), carts.end(), sort_carts);
		for (int i = 0; i < static_cast<int>(carts.size()); ++i)
		{
			cart& c = carts[i];
			if (!c.check)continue;
			switch (c.direction)
			{
			case 0:
				if (input_vec[c.y][c.x + 1] == '/')
				{
					c.direction = 3;
				}
				else if (input_vec[c.y][c.x + 1] == '\\')
				{
					c.direction = 1;
				}
				else if (input_vec[c.y][c.x + 1] == '+')
				{
					c.direction = (c.direction + 4 + c.last_intersection++) % 4;
					if (c.last_intersection > 1) c.last_intersection = -1;
				}
				++c.x;
				break;
			case 1:
				if (input_vec[c.y + 1][c.x] == '/')
				{
					c.direction = 2;
				}
				else if (input_vec[c.y + 1][c.x] == '\\')
				{
					c.direction = 0;
				}
				else if (input_vec[c.y + 1][c.x] == '+')
				{
					c.direction = (c.direction + 4 + c.last_intersection++) % 4;
					if (c.last_intersection > 1) c.last_intersection = -1;
				}
				++c.y;
				break;
			case 2:
				if (input_vec[c.y][c.x - 1] == '/')
				{
					c.direction = 1;
				}
				else if (input_vec[c.y][c.x - 1] == '\\')
				{
					c.direction = 3;
				}
				else if (input_vec[c.y][c.x - 1] == '+')
				{
					c.direction = (c.direction + 4 + c.last_intersection++) % 4;
					if (c.last_intersection > 1) c.last_intersection = -1;
				}
				--c.x;
				break;
			case 3:
				if (input_vec[c.y - 1][c.x] == '/')
				{
					c.direction = 0;
				}
				else if (input_vec[c.y - 1][c.x] == '\\')
				{
					c.direction = 2;
				}
				else if (input_vec[c.y - 1][c.x] == '+')
				{
					c.direction = (c.direction + 4 + c.last_intersection++) % 4;
					if (c.last_intersection > 1) c.last_intersection = -1;
				}
				--c.y;
				break;
			}

			if (collides(c, carts))
			{
				cart r = c;
				for (int j = 0; j < carts.size();++j)
				{
					if (carts[j].x == r.x && carts[j].y == r.y)
					{
						carts[j].check = false;
					}
				}
				int unchecked{ 0 };
				for (auto& a : carts)
				{
					if (a.check) unchecked++;
				}
				if (unchecked == 1) {
					for (auto& a : carts)
					{

						//E, sada problem je da mi ne izvrti jos jednu iteraciju, a oni zele da se izvti, tako da to manualno napravim
						if (a.check) std::cout << a.x << "," << a.y << '\n';
					}
					goto end;
				}
				std::cout << r.x << "," << r.y << '\n';
			}
		}
	}
	end:
	while (true);
}