//Advent of Code 2021 day 9
use std::fs::File;
use std::io::{BufRead, BufReader};

fn parse_input() -> Vec<Vec<usize>>{
    let filename = "AoC2021/solutions/09/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);

    return reader
        .lines()
        .map(|l| l
            .unwrap()
            .chars()
            .map(|c| c.to_digit(10).unwrap() as usize)
            .collect())
        .collect();
}

fn find_moves(map: &mut Vec<Vec<usize>>, dir: &mut Vec<Vec<usize>>) -> usize{
    let moves: [(i32, i32); 4] = [(0, -1), (1, 0), (0, 1), (-1, 0)];
    let mut moved: usize = 0;

    let size = (map[0].len(), map.len());

    for y in 0..size.1{
        for x in 0..size.0{
            if dir[y][x] != usize::MAX { continue }
            let height = map[y][x];
            for (i, (dx, dy)) in moves.iter().enumerate(){
                let ix = (x as i32) + dx;
                if ix < 0 || (size.0 as i32) <= ix {continue;}
                let iy = (y as i32) + dy;
                if iy < 0 || (size.1 as i32) <= iy {continue;}
                let (nx, ny) = (ix as usize, iy as usize);

                if map[ny][nx] < height{
                    dir[y][x] = i;
                    moved += 1;
                    continue;
                }
                if map[ny][nx] == height && dir[ny][nx] != usize::MAX{
                    dir[y][x] = i;
                    moved += 1;
                    continue;
                }
            }
        }
    }
    return moved;
}

pub fn solve() {
    let mut map: Vec<Vec<usize>> = parse_input();
    let mut dir: Vec<Vec<usize>> = map.iter().map(|v| v.iter().map(|_| usize::MAX).collect()).collect();

    while find_moves(&mut map, &mut dir) > 0 {}

    let mut total: usize = 0;
    for y in 0..map.len(){
        for x in 0..map[y].len(){
            if dir[y][x] == usize::MAX {
                total += map[y][x] + 1;
            }
        }
    }
    println!("First:  {}", total);

    let mut basin: Vec<Vec<usize>> = map.iter().map(|v| v.iter().map(|_| 1).collect()).collect();
    let moves: [(i32, i32); 4] = [(0, -1), (1, 0), (0, 1), (-1, 0)];
    let mut moved = true;
    while moved{
        moved = false;
        for y in 0..map.len(){
            for x in 0..map[y].len(){
                if map[y][x] == 9 {continue};
                if basin[y][x] == 0 {continue};
                if dir[y][x] == usize::MAX {continue};

                let (dx, dy) = moves[dir[y][x]];
                let nx = ((x as i32) + dx) as usize;
                let ny = ((y as i32) + dy) as usize;
                basin[ny][nx] += basin[y][x];
                basin[y][x] = 0;
                moved = true;
            }
        }
    }

    let mut basins: Vec<usize> = basin.iter().flatten().map(|&b| b).collect();
    basins.sort_by(|a, b| b.cmp(a));
    let second: usize = basins.iter().take(3).product();
    println!("Second: {}", second);
}
