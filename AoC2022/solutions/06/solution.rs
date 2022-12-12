//Advent of Code 2022 day 6
use std::fs::File;
use std::io::{BufRead, BufReader};

fn parse_input() -> Vec<String>{
    let filename = "AoC2022/solutions/06/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    let mut inputs: Vec<String> = Vec::new();

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
    println!("Second: {}", second);
}
