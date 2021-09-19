#include <string>
#include <iterator>
#include <iostream>
#include <vector>
#include <algorithm>
#include <map>
#include <numeric>
#include <fstream>

int find_fuel(int x, int y, int grid_serial_number)
{
	int rack_ID = x + 10;
	int power_level = rack_ID * y;
	power_level += grid_serial_number;
	power_level *= rack_ID;
	power_level /= 100;
	power_level %= 10;
	power_level -= 5;
	return power_level;
}

int main()
{
	std::ifstream is("input.txt");
	int grid_serial_number = 9306;
	int fuel[300][300];

	for(int i = 0; i < 300; ++i)
	{
		for (int j = 0; j < 300; ++j)
		{
			fuel[i][j] = find_fuel(i + 1, j + 1, grid_serial_number);
		}
	}

	int max = 0;
	int x, y, max_size;
	for(int size = 1; size <= 300; ++size)
	{
		for (int i = 0; i < 300 - size; ++i)
		{
			for (int j = 0; j < 300 - size; ++j)
			{
				int sum = 0;
				for (int i1 = 0; i1 < size; ++i1)
				{
					for (int j1 = 0; j1 < size; ++j1)
					{
						sum += fuel[i + i1][j + j1];
					}
				}
				if (sum > max)
				{
					x = i + 1; y = j + 1;
					max_size = size;
					max = sum;
				}
			}
		}
	}




	std::cout << x << ',' << y << ',' << max_size;
	while (true);
}