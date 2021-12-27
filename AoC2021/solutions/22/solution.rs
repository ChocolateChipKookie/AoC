//Advent of Code 2021 day 22
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::cmp::{max, min};
use regex::Regex;

#[derive(Debug, Copy, Clone)]
struct Cuboid{
    x: (i64, i64),
    y: (i64, i64),
    z: (i64, i64),
    state: bool
}

impl Cuboid {
    fn new(x: (i64, i64), y: (i64, i64), z: (i64, i64), state: bool) -> Cuboid{
        return Cuboid{x, y, z, state};
    }

    fn intersection(&self, other: &Cuboid) -> Option<Cuboid>{
        fn dim_intersection(n1: (i64, i64), n2: (i64, i64)) -> (i64, i64) {
            return  (max(n1.0, n2.0), min(n1.1, n2.1));
        }

        return if self.intersects(other) {
            Some(
                Cuboid::new(
                    dim_intersection(self.x, other.x),
                    dim_intersection(self.y, other.y),
                    dim_intersection(self.z, other.z),
                    true
                )
            )
        } else {
            None
        }
    }

    fn intersects(&self, other: &Cuboid) -> bool{
        fn axis_intersects(n1: (i64, i64), n2: (i64, i64)) -> bool{
            return max(n1.0, n2.0) <= min(n1.1, n2.1);
        }

        return
            axis_intersects(self.x, other.x) &&
            axis_intersects(self.y, other.y) &&
            axis_intersects(self.z, other.z);
    }

    fn volume(&self) -> i64{
        return (self.x.1 - self.x.0 + 1) * (self.y.1 - self.y.0 + 1) * (self.z.1 - self.z.0 + 1);
    }

    fn is_small(&self) -> bool {
        return  (self.x.0 - self.x.1).abs() <= 100
    }
}

fn parse_input() -> Vec<Cuboid>{
    let filename = "AoC2021/solutions/22/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    let regex = Regex::new("-?\\d+").unwrap();

    let mut inputs: Vec<Cuboid> = Vec::new();
    for line_i in reader.lines(){
        let line = line_i.unwrap();
        let mut tokens = line.split(" ");
        let state = tokens.next().unwrap();

        let mut n = regex
            .captures_iter(tokens.next().unwrap())
            .map(|c| c
                .get(0)
                .unwrap()
                .as_str()
                .parse::<i64>()
                .unwrap());

        inputs.push(Cuboid::new(
            (n.next().unwrap(), n.next().unwrap()),
            (n.next().unwrap(), n.next().unwrap()),
            (n.next().unwrap(), n.next().unwrap()),
            state == "on"));
    }

    return inputs;
}

fn count(all: &Vec<Cuboid>) -> i64 {
    let mut cuboids: Vec<Cuboid> = Vec::new();
    let mut to_add: Vec<Cuboid> = Vec::new();

    for update in all{
        to_add.clear();
        for cuboid in &cuboids{
            if update.intersects(cuboid){
                let mut intersection = update.intersection(cuboid).unwrap();
                intersection.state = !cuboid.state;
                to_add.push(intersection);
            }
        }
        to_add.iter().for_each(|c| cuboids.push(*c));
        if update.state{
            cuboids.push(*update);
        }
    }

    let mut volume = 0;
    for cube in cuboids {
        if cube.state{
            volume += cube.volume()
        }
        else {
            volume -= cube.volume()
        }
    }

    return volume;
}

pub fn solve() {
    let input = parse_input();
    let small: Vec<Cuboid> = input.iter().filter(|&c| c.is_small()).map(|c| c.clone()).collect();
    println!("First:  {}", count(&small));
    println!("Second: {}", count(&input));
}
