use std::collections::HashMap;
//Advent of Code 2021 day 10
use std::fs::File;
use std::io::{BufRead, BufReader};

fn parse_input() -> Vec::<Vec<char>>{
    let filename = "AoC2021/solutions/10/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    return reader
        .lines()
        .map(|s| s
            .unwrap()
            .chars()
            .collect())
        .collect();
}

pub fn solve() {
    let input = parse_input();
    let mut pairs: HashMap<char, char> = HashMap::from([('(', ')'), ('[', ']'), ('{', '}'), ('<', '>')]);
    let mut corruption: HashMap<char, usize> = HashMap::from([(')', 3), (']', 57), ('}', 1197), ('>', 25137)]);
    let mut autocomplete: HashMap<char, usize> = HashMap::from([('(', 1), ('[', 2), ('{', 3), ('<', 4)]);

    let mut first: usize = 0;
    let mut second: Vec<usize> = Vec::new();
    for line in input{
        let mut stack = Vec::<char>::new();
        let mut corrupted = false;
        for c in line{
            if pairs.contains_key(&c){
                stack.push(c);
            }
            else{
                let top = stack.pop().unwrap();
                let expected = *pairs.get(&top).unwrap();
                if expected != c{
                    first += corruption.get(&c).unwrap();
                    corrupted = true;
                    break;
                }
            }
        }
        if ! corrupted {
            // Reverse iterate over stack and fold
            let score = stack.iter().rev().fold(0, |acc, c| acc * 5 + autocomplete.get(c).unwrap());
            second.push(score);
        }
    }
    second.sort();

    println!("First:  {}", first);
    println!("Second: {}", second[second.len()/2]);
}
