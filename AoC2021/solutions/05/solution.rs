use std::fs::File;
use std::io::{BufRead, BufReader};
use std::collections::HashMap;
use std::cmp;

fn parse_input() -> Vec::<((i64, i64), (i64, i64))>{
    let filename = "AoC2021/solutions/05/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    let mut inputs = Vec::<((i64, i64), (i64, i64))>::new();

    fn to_int(s_num: &str) -> i64 {
        return s_num.parse::<i64>().unwrap()
    }

    for line in reader.lines(){
        let line = line.unwrap();
        let mut line = line.split(" -> ");
        let from: Vec<&str> = line.next().unwrap().split(",").collect();
        let to  : Vec<&str> = line.next().unwrap().split(",").collect();

        let entry = ((to_int(from[0]), to_int(from[1])), (to_int(to[0]), to_int(to[1])));
        inputs.push(entry);
    }

    return inputs;
}

pub fn solve() {
    let mut vents_vh  = HashMap::<(i64, i64), i64>::new();
    let mut vents_all = HashMap::<(i64, i64), i64>::new();

    for entry in parse_input(){
        let (start, end) = entry;
        let mut dx = end.0 - start.0;
        let mut dy = end.1 - start.1;
        let len = cmp::max(dx.abs(), dy.abs());
        dx /= len;
        dy /= len;

        let is_straight = dx == 0 || dy == 0;

        for d in 0..=len{
            let x = start.0 + d*dx;
            let y = start.1 + d*dy;
            let pos = (x, y);
            if is_straight {
                *vents_vh.entry(pos).or_insert(0) += 1;
            }
            *vents_all.entry(pos).or_insert(0) += 1;
        }
    }

    let first  = vents_vh .iter().filter(|&(_, v)| v > &1).count();
    let second = vents_all.iter().filter(|&(_, v)| v > &1).count();
    println!("First:  {}", first);
    println!("First:  {}", second);
}
