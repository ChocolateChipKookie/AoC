//Advent of Code 2021 day 13
use std::fs::File;
use std::io::{BufRead, BufReader};

fn parse_input() -> (Vec<(usize, usize)>, Vec<(char, usize)>){
    let filename = "AoC2021/solutions/13/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    let mut positions: Vec<(usize, usize)> = Vec::new();
    let mut folds: Vec<(char, usize)> = Vec::new();

    let mut parse_folds = false;
    for line_i in reader.lines(){
        let line = line_i.unwrap();
        if line.is_empty(){
            parse_folds = true;
            continue;
        }
        if ! parse_folds{
            let mut tokens = line.split(",");
            positions.push((
                tokens.next().unwrap().parse().unwrap(),
                tokens.next().unwrap().parse().unwrap()
            ))
        } else {
            let eq = line.split(" ").last().unwrap();
            let mut tokens = eq.split("=");
            folds.push((
                    tokens.next().unwrap().chars().next().unwrap(),
                    tokens.next().unwrap().parse().unwrap()
            ));
        }
    }

    return (positions, folds);
}

fn scatter(pos: &Vec<(usize, usize)>) -> (Vec<Vec<bool>>, usize, usize){
    let width = pos.iter().map(|t| t.0).max().unwrap() + 1;
    let height = pos.iter().map(|t| t.1).max().unwrap() + 1;
    let mut map = vec![vec![false; width]; height];
    for (x, y) in pos.iter(){
        map[*y][*x] = true;
    }
    return  (map, width, height);
}

fn fold(map: &mut Vec<Vec<bool>>, width: &mut usize, height: &mut usize, pos: usize, dim: char){
    if dim == 'x' {
        let to_copy = *width - pos;
        *width = pos;
        for y in 0..*height{
            for d in 1..to_copy{
                map[y][pos - d] |= map[y][pos + d];
            }
        }
    }
    else{
        let to_copy = *height - pos;
        *height = pos;

        for d in 1..to_copy{
            for x in 0..*width{
                map[pos - d][x] |= map[pos + d][x];
            }
        }
    }
}

pub fn solve() {
    let input = parse_input();
    let (mut map, mut width, mut height) = scatter(&input.0);

    let mut fold_iter = input.1.iter();
    let (dim , pos) = fold_iter.next().unwrap();

    fold(&mut map, &mut width, &mut height, *pos, *dim);
    let first: usize = (0..height).map(|y| (0..width).filter(|x| map[y][*x]).count()).sum();
    println!("First:  {}", first);

    for (dim, pos) in fold_iter{
        fold(&mut map, &mut width, &mut height, *pos, *dim);
    }
    println!("Second: ");
    for y in 0..height{
        println!("{}", (0..width).map(|x| if map[y][x] {'#'} else {' '}).collect::<String>());
    }
}
