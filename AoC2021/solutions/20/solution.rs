use std::collections::HashSet;
//Advent of Code 2021 day 20
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::mem::swap;

fn parse_input() -> (String, Vec<Vec<char>>){
    let filename = "AoC2021/solutions/20/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    let mut lines = reader.lines();
    let rules = lines.next().unwrap().unwrap();
    lines.next();

    let mut inputs: Vec<Vec<char>> = Vec::new();
    for line in lines{
        inputs.push(line.unwrap().chars().collect());
    }

    return (rules, inputs);
}

fn step(points: &mut HashSet<(i32, i32)>, points_swap: &mut HashSet<(i32, i32)>, rules: &Vec<bool>, dims: ((i32, i32), (i32, i32)), default: char) -> char{
    points_swap.clear();

    let get_pixel = |x: i32, y: i32| {
        if (dims.0.0..=dims.1.0).contains(&x) && (dims.0.1..=dims.1.1).contains(&y){
            return points.contains(&(x, y));
        }
        return default == '#';
    };

    let get_num = |x: i32, y: i32| {
        let mut factor = 256;
        let mut total = 0;
        for dy in -1..=1{
            for dx in -1..=1{
                if get_pixel(x + dx, y + dy){
                    total += factor;
                }
                factor /= 2;
            }
        }
        return total;
    };

    for y in dims.0.1..=dims.1.1{
        for x in dims.0.1..=dims.1.1{
            if rules[get_num(x, y) as usize]{
                points_swap.insert((x, y));
            }
        }
    }
    swap(points_swap, points);

    return
        if default == '.' {
            if rules[0] { '#' } else { '.' }
        } else {
            if *rules.last().unwrap() { '#' } else { '.' }
        }
}

pub fn solve() {
    let (rules_string, image) = parse_input();
    let mut points: HashSet<(i32, i32)> = HashSet::new();
    let mut points_swap: HashSet<(i32, i32)> = HashSet::new();
    let height = image.len();
    let width = image[0].len();
    for y in 0..height{
        for x in 0..width{
            if image[y][x] == '#'{
                points.insert((x as i32, y as i32));
            }
        }
    }

    let mut default = '.';
    let mut dims = ((-1, -1), (width as i32, height as i32));
    let rules: Vec<bool> = rules_string.chars().map(|c| c == '#').collect();

    fn extend_dims(points: &mut HashSet<(i32, i32)>, dims: &mut ((i32, i32), (i32, i32)), default: char){
        dims.0.0 -= 1;
        dims.0.1 -= 1;
        dims.1.0 += 1;
        dims.1.1 += 1;
        if default == '#' {
            for x in dims.0.0..=dims.1.0{
                points.insert((x, dims.0.1));
                points.insert((x, dims.1.1));
            }
            for y in dims.0.1..=dims.1.1{
                points.insert((dims.0.0, y));
                points.insert((dims.1.0, y));
            }
        }
    };

    for _ in 0..2 {
        default = step(&mut points, &mut points_swap, &rules, dims, default);
        extend_dims(&mut points, &mut dims, default);
    }
    println!("First:  {}", points.len());
    for _ in 2..50 {
        default = step(&mut points, &mut points_swap, &rules, dims, default);
        extend_dims(&mut points, &mut dims, default);
    }
    println!("Second: {}", points.len());
}
