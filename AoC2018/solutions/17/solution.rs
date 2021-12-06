//Advent of Code 2018 day 17
use std::fs::File;
use std::io::{BufRead, BufReader};

fn parse_input() -> Vec::<str>{
    let filename = "AoC2018/solutions/17/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    let mut inputs = Vec::<str>::new();

    for line in reader.lines(){
        inputs.push(line.unwrap());
    }

    return inputs;
}

pub fn solve() {
    let input = parse_input();
    
    let first  = 0;
    let second = 0;
    println!("First:  {}", first);
    println!("First:  {}", second);
}
