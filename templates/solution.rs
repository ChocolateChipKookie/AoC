//Advent of Code {year} day {day}
use std::fs::File;
use std::io::{{BufRead, BufReader}};

fn parse_input() -> Vec::<String>{{
    let filename = "AoC{year}/solutions/{filled}/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    let mut inputs = Vec::<String>::new();

    for line in reader.lines(){{
        inputs.push(line.unwrap());
    }}

    return inputs;
}}

pub fn solve() {{
    let input = parse_input();
    
    let first  = 0;
    let second = 0;
    println!("First:  {{}}", first);
    println!("Second: {{}}", second);
}}
