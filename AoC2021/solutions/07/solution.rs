//Advent of Code 2021 day 7
use std::fs::File;
use std::io::{BufRead, BufReader};

fn parse_input() -> Vec::<i64>{
    let filename = "AoC2021/solutions/07/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);

    let input_line = reader.lines().next().unwrap().unwrap();
    let data: Vec::<i64> = input_line.split(",").map(|x| x.parse::<i64>().unwrap()).collect();

    return data;
}

pub fn solve() {

    fn calc_uniform(data: &Vec<i64>, pos: i64) -> i64 {
        return data.iter().map(|x| (x - pos).abs()).sum::<i64>();
    }

    fn calc_rising(data: &Vec<i64>, pos: i64) -> i64 {
        fn sum_n(n: i64) -> i64{
            return n * (n + 1) / 2;
        }
        return data.iter().map(|x| sum_n((x - pos).abs())).sum::<i64>();
    }

    fn bisect(mut lo: i64, mut hi: i64, data: &Vec<i64>, pred: &dyn Fn(&Vec<i64>, i64) -> i64) -> i64{
        while lo < hi{
            let mid = (lo + hi) / 2;
            if pred(&data, mid) < pred(&data, mid + 1){
                hi = mid;
            }
            else{
                lo = mid + 1;
            }
        }
        return pred(&data, lo);
    }

    let data = parse_input();
    let min: i64 = *data.iter().min().unwrap();
    let max: i64 = *data.iter().max().unwrap();

    let first  = bisect(min, max, &data, &calc_uniform);
    let second = bisect(min, max, &data, &calc_rising);
    println!("First:  {}", first);
    println!("Second: {}", second);
}
