//Advent of Code 2018 day 18
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::mem;
use std::collections::HashMap;

fn print_map(map: &Vec<Vec<char>>){
    for line in map{
        for c in line{
            print!("{}", c);
        }
        print!("\n");
    }
}
fn parse_input() -> Vec<Vec<char>>{
    let filename = "AoC2018/solutions/18/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    return reader.lines().map(|s| s.unwrap().chars().collect()).collect();
}

fn do_gen(current: &mut Vec<Vec<char>>, swap: &mut Vec<Vec<char>>){

    fn count(current: &mut Vec<Vec<char>>, x: usize, y:usize, state: char) -> usize{
        let min_y = if y == 0 { 0 } else { y - 1 };
        let max_y = if y == current.len() - 1 { y } else { y + 1 };
        let min_x = if x == 0 { 0 } else { x - 1 };
        let max_x = if x == current[0].len() - 1 { x } else { x + 1 };

        let mut total = 0;
        for ny in min_y..=max_y{
            for nx in min_x..=max_x{
                if nx == x && ny == y{
                    continue;
                }
                if current[ny][nx] == state{
                    total += 1;
                }
            }
        }
        return total;
    }

    for y in 0..current.len(){
        for x in 0.. current[y].len(){
            let state = current[y][x];
            match state {
                '.' => {
                    if count(current, x, y, '|') >= 3{
                        swap[y][x] = '|';
                    }
                    else {
                        swap[y][x] = '.';
                    }
                },
                '|' => {
                    if count(current, x, y, '#') >= 3{
                        swap[y][x] = '#';
                    }
                    else {
                        swap[y][x] = '|';
                    }
                },
                '#' => {
                    if count(current, x, y, '#') >= 1 && count(current, x, y, '|') >= 1{
                        swap[y][x] = '#';
                    }
                    else {
                        swap[y][x] = '.';
                    }
                },
                _ => {}
            }
        }
    }

    mem::swap(current, swap);
}

fn first() -> usize{
    let mut data: Vec<Vec<char>> = parse_input();
    let mut swap: Vec<Vec<char>> = data.iter().map(|x| x.clone()).collect();

    print_map(&data);
    for i in 0..10{
        do_gen(&mut data, &mut swap);
        println!("{}", i);
        print_map(&data);
    }
    let wood       : usize = data.iter().map(|r| r.iter().filter(|&&c| c == '|').count()).sum();
    let lumberyard : usize = data.iter().map(|r| r.iter().filter(|&&c| c == '#').count()).sum();

    return wood * lumberyard;
}

fn second() -> usize {
    let mut data: Vec<Vec<char>> = parse_input();
    let mut swap: Vec<Vec<char>> = data.iter().map(|x| x.clone()).collect();
    let mut history = HashMap::<String, usize>::new();
    let total_minutes = 1000000000;
    let mut period = 0;
    let mut minute = 0;

    fn to_str(current: &mut Vec<Vec<char>>) -> String{
        let mut res = String::with_capacity(current.len() * current[0].len());
        for line in current{
            for c in line{
                res.push(*c);
            }
        }
        return res;
    }

    history.insert(to_str(&mut data), 0);
    for i in 0..total_minutes{
        do_gen(&mut data, &mut swap);
        let repr = to_str(&mut data);
        if history.contains_key(&repr){
            period = i - history.get(&repr).unwrap();
            minute = i;
            break;
        }
        history.insert(repr, i);
    }

    let cycles = (total_minutes - minute) / period;
    let remaining = total_minutes - minute - period * cycles;
    let prev_same = minute - (period - remaining) - 1;

    let repr = history.iter().find(|entry| *entry.1 == prev_same).unwrap().0;
    let wood       : usize = repr.chars().filter(|&c| c == '|').count();
    let lumberyard : usize = repr.chars().filter(|&c| c == '#').count();

    return wood * lumberyard;
}

pub fn solve() {
    println!("First:  {}", first());
    println!("Second: {}", second());
}
