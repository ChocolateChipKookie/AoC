//Advent of Code 2021 day 8
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::collections::HashSet;
use std::hash::Hash;

fn parse_input() -> Vec::<String>{
    let filename = "AoC2021/solutions/08/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    let mut inputs = Vec::<String>::new();

    for line in reader.lines(){
        inputs.push(line.unwrap());
    }

    return inputs;
}

fn first(data: &Vec<String>) -> usize{
    return data .iter()
                .map(|x| x
                    .split(" | ")
                    .last()
                    .unwrap())
                .map(|x| x
                    .split(" ")
                    .filter(|&s| s.len() <= 4 || s.len() == 7)
                    .count())
                .sum();
}

fn second(data: &Vec<String>) -> usize{
    fn calc(data: &String) -> usize {
        let values: Vec<&str> = data.split(" ").filter(|x| x.len() > 1).collect();
        let one = values.iter().find(|x| x.len() == 2).unwrap();
        let four = values.iter().find(|x| x.len() == 4).unwrap();
        let seven = values.iter().find(|x| x.len() == 3).unwrap();
        let eight = values.iter().find(|x| x.len() == 7).unwrap();

        let one_s: HashSet<char> = one.chars().collect();
        let four_s: HashSet<char> = four.chars().collect();
        let seven_s: HashSet<char> = seven.chars().collect();
        let eight_s: HashSet<char> = eight.chars().collect();
        let d41: HashSet<char> = four_s.difference(&one_s).map(|&c| c).collect();
        let u47: HashSet<char> = seven_s.union(&four_s).map(|&c| c).collect();

        let nine = values
            .iter()
            .filter(|x| x.len() == 6)
            .find(|x| x.chars().collect::<HashSet<char>>().union(&four_s).count() == 6)
            .unwrap();
        let zero = values
            .iter()
            .filter(|x| x.len() == 6)
            .find(|x| x.chars().collect::<HashSet<char>>().union(&d41).count() == 7)
            .unwrap();
        let six = values
            .iter()
            .filter(|x| x.len() == 6)
            .find(|&x| x != zero && x != nine)
            .unwrap();

        let zero_s: HashSet<char> = zero.chars().collect();
        let six_s: HashSet<char> = six.chars().collect();
        let nine_s: HashSet<char> = nine.chars().collect();

        let a: char = *seven_s.difference(&one_s).next().unwrap();
        let d: char = *eight_s.difference(&zero_s).next().unwrap();
        let b: char = *d41.iter().filter(|&&b| b != d).next().unwrap();
        let c: char = *eight_s.difference(&six_s).next().unwrap();
        let e: char = *eight_s.difference(&nine_s).next().unwrap();
        let f: char = *one_s.iter().filter(|&&f| f != c).next().unwrap();
        let g: char = *nine_s.difference(&u47).next().unwrap();

        let two_s: HashSet<char> = vec![a, c, d, e, g].iter().map(|&c| c).collect();
        let three_s: HashSet<char> = vec![a, c, d, f, g].iter().map(|&c| c).collect();
        let five_s: HashSet<char> = vec![a, b, d, f, g].iter().map(|&c| c).collect();

        let sets: Vec<&HashSet<char>>= vec![&zero_s, &one_s, &two_s, &three_s, &four_s, &five_s, &six_s, &seven_s, &eight_s, &nine_s];

        let mut res: usize = 0;
        for value in data.split(" | ").last().unwrap().split(" "){
            let val_s: HashSet<char> = value.chars().collect();
            res *= 10;
            for (i, num_s) in sets.iter().enumerate(){
                if num_s == &&val_s{
                    res += i;
                    break;
                }
            }
        }

        return res;
    }

    return data.iter().map(|x| calc(x)).sum();
}

pub fn solve() {
    let input = parse_input();

    println!("First:  {}", first(&input));
    println!("Second: {}", second(&input));
}
