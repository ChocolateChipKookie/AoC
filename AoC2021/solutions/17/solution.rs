use std::cmp::max;
//Advent of Code 2021 day 17
use std::fs::File;
use std::io::{BufRead, BufReader};
use regex::Regex;

fn parse_input() -> ((i64, i64), (i64, i64)){
    let filename = "AoC2021/solutions/17/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    let line_i = reader.lines().next().unwrap().unwrap();
    let line = line_i.as_str();
    let regex = Regex::new("-?\\d+").unwrap();
    let mut n = regex
        .captures_iter(line)
        .map(|c| c
            .get(0)
            .unwrap()
            .as_str()
            .parse::<i64>()
            .unwrap());

    return ((n.next().unwrap(), n.next().unwrap()), (n.next().unwrap(), n.next().unwrap()));
}

fn first() -> i64{
    let (_x, y) = parse_input();
    let depth = -y.0;
    return depth * (depth - 1) / 2;
}

fn second() -> usize{
    let (x_dim, y_dim) = parse_input();
    let min_x = (((1. + 8. * (x_dim.0 as f64)).sqrt() - 1.) / 2.).floor() as i64;
    let max_x = x_dim.1;
    let min_y = y_dim.0;
    let max_y = -y_dim.0;

    fn will_hit(mut vx: i64, mut vy: i64, x_dim: &(i64, i64), y_dim: &(i64, i64)) -> bool{
        let mut x = vx;
        let mut y = vy;

        loop {
            if (x > x_dim.1) || (y < y_dim.0) || (vx == 0 && x < x_dim.0){
                return false;
            }

            if x >= x_dim.0 && y <= y_dim.1{
                return true;
            }

            vx = max(vx - 1, 0);
            vy -= 1;
            x += vx;
            y += vy;
        }
    }


    let mut count = 0;
    for y in min_y..=max_y{
        for x in min_x..=max_x{
            if will_hit(x, y, &x_dim, &y_dim){
                count += 1;
            }
        }
    }

    return count;
}

pub fn solve() {
    println!("First:  {}", first());
    println!("Second: {}", second());
}
