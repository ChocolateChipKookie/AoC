//Advent of Code 2018 day 20
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::str::Chars;

fn parse_input() -> String{
    let filename = "AoC2018/solutions/20/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    return reader.lines().next().unwrap().unwrap();
}

fn recurse(pos: (i32, i32), known: &mut Vec<((i32, i32), char)>, stream: &mut Chars) -> bool{


    return true;
}

fn expand_map(regex: String){
    let mut char_iter = regex.chars();
    let mut known: Vec<((i32, i32), char)> = Vec::new();
    recurse(&mut known, &mut char_iter);

}

pub fn solve() {
    let input = parse_input();
    println!("{}", input);


    let first  = 0;
    let second = 0;
    println!("First:  {}", first);
    println!("Second: {}", second);
}
