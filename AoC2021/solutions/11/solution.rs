//Advent of Code 2021 day 11
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::cmp::{max, min};

fn parse_input() -> Vec<Vec<usize>>{
    let filename = "AoC2021/solutions/11/input";
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

pub fn solve() {
    let mut map = parse_input();
    let mut flashed: Vec<Vec<bool>> = map.iter().map(|r| r.iter().map(|_| false).collect()).collect();
    let steps = 100;

    fn increment(map: &mut Vec<Vec<usize>>){
        for y in 0..map.len(){
            for x in 0..map[y].len(){
                map[y][x] += 1;
            }
        }
    }

    fn flash(map: &mut Vec<Vec<usize>>, flashed: &mut Vec<Vec<bool>>) -> usize{
        for row in flashed.iter_mut(){
            row.fill(false);
        }

        fn do_flash(map: &mut Vec<Vec<usize>>, x: usize, y: usize){
            let x_min = max(0, (x as i32) - 1) as usize;
            let x_max = min(map[0].len(), x + 2);
            let y_min = max(0, (y as i32) - 1) as usize;
            let y_max = min(map.len(), y + 2);
            for y in y_min..y_max{
                for x in x_min..x_max{
                    map[y][x] += 1;
                }
            }
        }

        let mut flashes = 0;
        let mut run = true;
        while run {
            run = false;
            for y in 0..map.len(){
                for x in 0..map[y].len(){
                    if !flashed[y][x] && map[y][x] > 9{

                        do_flash(map, x, y);
                        flashed[y][x] = true;
                        run = true;
                        flashes += 1;
                    }
                }
            }
        }
        for y in 0..map.len(){
            for x in 0..map[y].len(){
                if map[y][x] > 9{
                    map[y][x] = 0;
                }
            }
        }

        return flashes;
    }

    let mut first = 0;
    for _ in 0..steps{
        increment(&mut map);
        first += flash(&mut map, &mut flashed);
    }

    let mut second = steps;
    loop {
        increment(&mut map);
        flash(&mut map, &mut flashed);
        second += 1;
        let sum: usize = map.iter().map(|r| r.iter().sum::<usize>()).sum();
        if sum == 0{
            break;
        }
    }

    println!("First:  {}", first);
    println!("Second: {}", second);
}
