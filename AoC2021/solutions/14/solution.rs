//Advent of Code 2021 day 14
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::collections::HashMap;

fn parse_input() -> (Vec<char>, HashMap<(char, char), char>){
    let filename = "AoC2021/solutions/14/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    let mut  line_iterator = reader.lines();

    let mut combinations: HashMap<(char, char), char> = HashMap::new();
    let input_polymer: Vec<char> = line_iterator.next().unwrap().unwrap().chars().collect();

    // Skip empty line
    line_iterator.next();

    for line_i in line_iterator{
        let line = line_i.unwrap();
        let mut tokens = line.split(" -> ");
        let mut seed_i = tokens.next().unwrap().chars();

        let seed = (seed_i.next().unwrap(), seed_i.next().unwrap());
        let result = tokens.next().unwrap().chars().next().unwrap();
        combinations.insert(seed, result);
    }

    return (input_polymer, combinations);
}

fn combine(m1: &HashMap<char, usize>, m2: &HashMap<char, usize>) -> HashMap<char, usize>{
    let mut dest = m1.clone();
    for (&key, &val) in m2.iter(){
        *dest.entry(key).or_insert(0) += val;
    }
    return dest;
}

fn recurse(first: char, second: char, depth: usize, rules: &HashMap<(char, char), char>, calculated: &mut HashMap<(char, char, usize), HashMap<char, usize>>){
    if calculated.contains_key(&(first, second, depth)) {
        return;
    }
    let mid = *rules.get(&(first, second)).unwrap();

    if depth <= 1 {
        calculated.insert((first, second, depth), HashMap::from([(mid, 1)]));
        return;
    }

    let mid = *rules.get(&(first, second)).unwrap();
    recurse(first, mid, depth - 1, rules, calculated);
    recurse(mid, second, depth - 1, rules, calculated);

    let child1 = calculated.get(&(first, mid, depth - 1)).unwrap();
    let child2 = calculated.get(&(mid, second, depth - 1)).unwrap();
    let mut combined = combine(child1, child2);
    *combined.entry(mid).or_insert(0) += 1;
    calculated.insert((first, second, depth), combined);
}

fn calc(steps: usize) -> usize{
    let (polymer, rules) = parse_input();
    let mut calculated: HashMap<(char, char, usize), HashMap<char, usize>> = HashMap::new();

    for i in 1..polymer.len(){
        recurse(polymer[i-1], polymer[i], steps, &rules, &mut calculated);
    }

    let mut counts = calculated
        .iter()
        .filter(|e| e.0.2 == steps)
        .fold(HashMap::new(), |acc, v| combine(&acc, v.1));

    for c in polymer{
        *counts.entry(c).or_insert(0) += 1;
    }

    let max = counts.iter().map(|t| t.1).max().unwrap();
    let min = counts.iter().map(|t| t.1).min().unwrap();

    return max - min;
}

pub fn solve() {
    println!("First:  {}", calc(10));
    println!("Second: {}", calc(40));
}
