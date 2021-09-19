#include <string>
#include <iterator>
#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <thread>

using pair = std::pair<int, int>;

struct star{
	pair pos,speed;
};

struct boundries{
	pair x, y;
};

void update_stars(std::vector<star>& stars, int time){
	for (auto& star : stars)
	{
		star.pos.first += star.speed.first * time;
		star.pos.second += star.speed.second * time;
	}
}

boundries find_min_max(std::vector<star>& stars){
	boundries b = { { 100000, -1000000 } , { 100000, -1000000 } };
	for (auto& star : stars){
		if (star.pos.first < b.x.first) b.x.first = star.pos.first;
		else if (star.pos.first > b.x.second) b.x.second = star.pos.first;
		if (star.pos.second < b.y.first) b.y.first = star.pos.second;
		else if (star.pos.second > b.y.second) b.y.second = star.pos.second;
	}
	return b;
}

void print_stars(std::vector<star>& stars){
	const boundries b{ find_min_max(stars) };

	for(int i = b.y.first; i <=b.y.second; ++i){
		for (int j = b.x.first; j <= b.x.second; ++j){
			bool star = false;
			for (auto& s : stars){
				if (s.pos.first == j && s.pos.second == i) star = true;
			}

			if (star)std::cout << '#';
			else std::cout << ' ';
		}
		std::cout << '\n';
	}
}

int f_dist(std::pair<int, int> i){
	return i.second - i.first;
}

int main()
{
	std::ifstream is("input.txt");
	std::vector<star> stars;

	std::vector<std::string> input_vec;for (std::string l; std::getline(is, l); ) { 
		std::istringstream iss{ l };
		star st;
		iss >> st.pos.first >> st.pos.second >> st.speed.first >> st.speed.second;
		stars.emplace_back(st);
	}

	int prev_dist = f_dist(find_min_max(stars).x);
	int dist;
	for(int i = 0;;++i){
		if ((dist = f_dist(find_min_max(stars).x)) > prev_dist) { std::cout << --i << '\n'; break; }
		prev_dist = dist;
		update_stars(stars, 1);
	}
	update_stars(stars, -1);
	print_stars(stars);
	while (true);
}