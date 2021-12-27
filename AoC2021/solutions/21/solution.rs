//Advent of Code 2021 day 21
use std::fs::File;
use std::io::{BufRead, BufReader};

use std::collections::HashMap;

fn parse_input() -> (usize, usize){
    let filename = "AoC2021/solutions/21/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    let mut lines = reader.lines();

    let first = lines.next().unwrap().unwrap().split(" ").last().unwrap().parse().unwrap();
    let second = lines.next().unwrap().unwrap().split(" ").last().unwrap().parse().unwrap();

    return (first, second);
}

fn first(){
    let input = parse_input();
    let mut dice_count: usize = 0;
    let mut roll = ||{
        let v = dice_count % 100 + 1;
        dice_count += 1;
        return v;
    };

    let mut pos: [usize; 2] = [input.0 - 1, input.1 - 1];
    let mut score: [usize; 2] = [0, 0];
    let mut turn = 0;
    let limit = 1000;
    loop {
        let rolls = roll() + roll() + roll();

        let player = turn % 2;
        pos[player] = (pos[player] + rolls) % 10;
        score[player] += pos[player] + 1;

        if score[player] >= limit { break }
        turn += 1;
    }
    let loser = (turn + 1) % 2;

    println!("First:  {}", dice_count * score[loser]);
}

fn second(){
    let input = parse_input();
    let dist: Vec<usize> = Vec::from([0, 0, 0, 1, 3, 6, 7, 6, 3, 1]);

    // ((Pos, score), universes)
    // p0, p1
    let mut universes: Vec<HashMap<([(usize, usize); 2]), usize>> = Vec::from([HashMap::new()]);
    universes[0].insert([(input.0, 0), (input.1, 0)], 1);

    let win_score = 21;
    let mut wins: [usize; 2] = [0; 2];
    loop {
        let mut step: HashMap<([(usize, usize); 2]), usize> = HashMap::new();

        for (data, prev_count) in universes.last().unwrap(){
            let (pos_0, score_0) = data[0];
            let (pos_1, score_1) = data[1];

            for (steps_0, permutations_0) in dist.iter().enumerate().skip(3){
                let npos_0 = (pos_0 - 1 + steps_0) % 10 + 1;
                let nscore_0 = score_0 + npos_0;

                let ways_0 = prev_count * permutations_0;
                if nscore_0 >= win_score{
                    wins[0] += ways_0;
                    continue;
                }

                for (steps_1, permutations_1) in dist.iter().enumerate().skip(3){
                    let npos_1 = (pos_1 - 1 + steps_1) % 10 + 1;
                    let nscore_1 = score_1 + npos_1;
                    let ways_1 = prev_count * permutations_0 * permutations_1;
                    if nscore_1 >= win_score{
                        wins[1] += ways_1;
                        continue;
                    }
                    *step.entry([(npos_0, nscore_0), (npos_1, nscore_1)]).or_insert(0) += ways_1;
                }
            }
        }

        if step.is_empty() {
            break;
        }
        universes.push(step);
    }

    println!("Second: {}", wins.iter().max().unwrap());
}


pub fn solve() {
    first();
    second();
}
