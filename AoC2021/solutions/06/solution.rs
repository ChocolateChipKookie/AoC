//Advent of Code 2021 day 6
use std::fs::File;
use std::io::{BufRead, BufReader};

fn parse_input() -> Vec::<i64>{
    let filename = "AoC2021/solutions/06/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);

    let input_line = reader.lines().next().unwrap().unwrap();
    let data: Vec::<i64> = input_line.split(",").map(|x| x.parse::<i64>().unwrap()).collect();

    return data;
}

pub fn solve() {
    // Ages of the start population
    let input  = parse_input();
    // Ages
    let adult  = 6;
    let birth  = adult + 2;
    // Cycle len
    let cycles = 80;
    let cycles_long = 256;
    // Population by age
    let mut population: Vec::<i64> = vec![0; birth + 1];
    for age in input {
        population[age as usize] += 1;
    }
    
    // First part
    for _ in 0..cycles{
        let new_fish = population[0];
        population.rotate_left(1);
        population[adult as usize] += new_fish;
    }
    let first: i64 = population.iter().sum();

    // Continue with second part
    for _ in 0..(cycles_long - cycles){
        let new_fish = population[0];
        population.rotate_left(1);
        population[adult as usize] += new_fish;
    }

    let second: i64 = population.iter().sum();
    println!("First:  {}", first);
    println!("Second: {}", second);
}
