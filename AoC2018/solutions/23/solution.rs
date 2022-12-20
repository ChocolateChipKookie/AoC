use std::f64::consts::PI;
//Advent of Code 2018 day 23
use std::fs::File;
use std::io::{BufRead, BufReader};
use regex::Regex;


#[derive(Debug, Copy, Clone)]
struct Nanobot{
    x: i64,
    y: i64,
    z: i64,
    radius: i64
}

impl Nanobot {
    fn new(x: i64, y: i64, z: i64, radius: i64) -> Nanobot{
        return Nanobot{x, y, z, radius};
    }

    fn in_range(&self, other: &Nanobot) -> bool{
        let dist: i64 =
            (self.x - other.x).abs() +
            (self.y - other.y).abs() +
            (self.z - other.z).abs();
        return dist <= self.radius;
    }

    fn intersects(&self, other: &Nanobot) -> bool {
        let x_diff = (self.x - other.x).abs();
        let y_diff = (self.y - other.y).abs();
        let z_diff = (self.z - other.z).abs();
        return (x_diff + y_diff + z_diff) <= (self.radius + other.radius);
    }
}


fn parse_input() -> Vec<Nanobot>{
    let filename = "AoC2018/solutions/23/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    let mut inputs: Vec<Nanobot> = Vec::new();
    let regex = Regex::new("-?\\d+").unwrap();

    for line_i in reader.lines(){
        let line: String = line_i.unwrap();
        let mut n = regex
            .captures_iter(&line)
            .map(|c| c
                .get(0)
                .unwrap()
                .as_str()
                .parse::<i64>()
                .unwrap());

        inputs.push(Nanobot::new(
            n.next().unwrap(),
            n.next().unwrap(),
            n.next().unwrap(),
            n.next().unwrap()
        ));
    }

    return inputs;
}

pub fn solve() {
    let input: Vec<Nanobot> = parse_input();

    let max_radius = input.iter().map(|n| n.radius).max().unwrap();
    let bot = input.iter().find(|n| n.radius == max_radius).unwrap();

    let first  = input.iter().filter(|n| bot.in_range(n)).count();

    let mut counter: Vec<i64> = Vec::new();

    for n1 in &input{
        let mut count = 0;
        for n2 in &input{
            if n1.intersects(&n2){
                count += 1;
            }
        }
        counter.push(count);
    }

    let second = 0;
    println!("First:  {}", first);
    println!("Second: {}", second);
}
