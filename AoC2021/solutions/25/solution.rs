//Advent of Code 2021 day 25
use std::fs::File;
use std::io::{BufRead, BufReader};

fn parse_input() -> Vec<Vec<char>>{
    let filename = "AoC2021/solutions/25/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    let mut inputs: Vec<Vec<char>> = Vec::new();

    for line in reader.lines(){
        inputs.push(line.unwrap().chars().collect());
    }

    return inputs;
}

pub fn solve() {
    let mut map = parse_input();

    fn try_move(map: &mut Vec<Vec<char>>, value: char, moves: &mut Vec<((usize, usize), (usize, usize))>) -> bool{
        moves.clear();
        let height = map.len();
        let width = map[0].len();
        for y in 0..height{
            for x in 0..width{
                if map[y][x] != value { continue };
                let next =
                    match map[y][x] {
                        '>' => ((x + 1) % width, y),
                        'v' => (x, (y + 1) % height),
                        _ => panic!("Wrong input!")
                    };
                if map[next.1][next.0] != '.' { continue }
                moves.push(((x, y), next));
            }
        }
        if moves.is_empty() { return false; }

        for (pos, npos) in moves {
            let val = map[pos.1][pos.0];
            map[pos.1][pos.0] = '.';
            map[npos.1][npos.0] = val;
        }

        return true;
    }

    let mut moves = Vec::<((usize, usize), (usize, usize))>::new();
    let mut first = 0;
    loop {
        let moved_east  = try_move(&mut map, '>', &mut moves);
        let moved_south = try_move(&mut map, 'v', &mut moves);

        first += 1;
        if !(moved_east || moved_south) {
            break;
        }
    }

    println!("First:  {}", first);
    println!("Second: PROFIT");
}
