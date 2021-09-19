#include <string>
#include <iostream>
#include <vector>
#include <algorithm>
#include <fstream>
#include <list>
#include <chrono>
#include <memory_resource>

using list_iterator = std::list<unsigned>::iterator;
using list = std::pmr::list<unsigned>;

list_iterator circle_around(list_iterator it, list& list, int moveAmount){
	if(moveAmount < 0)
		for(int i = 0; i > moveAmount; --i){
			if(it == list.begin())
				it = list.end();
			--it;
		}
	else
		for (int i = 0; i < moveAmount; ++i)
			if (++it == list.end())
				it = list.begin();
	return it;
}

int main(){
	
	auto start = std::chrono::high_resolution_clock::now();

	std::ifstream is("input.txt");
	int players, marble_count;
	is >> players >> marble_count;

	std::vector<unsigned> player_scores(players + 1, 0);
	auto resource = std::pmr::monotonic_buffer_resource( marble_count * 50); // ~160 ms
	list marbles(&resource);
	marbles.emplace_back(0);
	auto pos = marbles.begin();

	for (int i = 1, k = marble_count * 100; i <= k; ++i) {
		if (i % 23 == 0) {
			const auto tmp = circle_around(pos, marbles, -7);
			player_scores[i % players] += i + *tmp;
			marbles.erase(tmp);
			pos = circle_around(pos, marbles, -6);
}
		else {
			marbles.insert(circle_around(pos, marbles, 2), i);
			pos = circle_around(pos, marbles, 2);
		}
}

	auto finish = std::chrono::high_resolution_clock::now();
	std::chrono::duration<double> elapsed = finish - start;
	const auto tmp{ std::max_element(player_scores.begin(), player_scores.end()) };
	std::cout << *tmp << '\n' << elapsed.count() << '\n';
	while (true);
}