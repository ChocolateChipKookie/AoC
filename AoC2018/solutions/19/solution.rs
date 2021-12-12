//Advent of Code 2018 day 19
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::collections::HashMap;

fn parse_input() -> (usize, Vec::<(String, usize, usize, usize)>){
    let filename = "AoC2018/solutions/19/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    let mut inputs = Vec::<(String, usize, usize, usize)>::new();
    let mut ip: usize = 0;
    for (i, line_i) in reader.lines().enumerate(){
        if i == 0 {
            ip = line_i.unwrap().split(" ").last().unwrap().parse().unwrap();
            continue;
        }
        let line = line_i.unwrap();
        let mut tokens = line.split(" ");
        let command = tokens.next().unwrap().to_string();
        let a1: usize = tokens.next().unwrap().parse().unwrap();
        let a2: usize = tokens.next().unwrap().parse().unwrap();
        let a3: usize = tokens.next().unwrap().parse().unwrap();
        inputs.push((command, a1, a2, a3));
    }

    return (ip, inputs);
}

fn map_functions() -> HashMap<String, Box<dyn Fn(usize, usize, usize, &mut Vec<usize>) -> ()>>{
    let mut functions: HashMap<String, Box<dyn Fn(usize, usize, usize, &mut Vec<usize>) -> ()>> = HashMap::new();
    functions.insert("addr".to_string(), Box::new(|a: usize, b: usize, c: usize, r: &mut Vec<usize>|
        {r[c as usize] = r[a as usize] + r[b as usize]}));
    functions.insert("addi".to_string(), Box::new(|a: usize, b: usize, c: usize, r: &mut Vec<usize>|
        {r[c as usize] = r[a as usize] + b}));

    functions.insert("mulr".to_string(), Box::new(|a: usize, b: usize, c: usize, r: &mut Vec<usize>|
        {r[c as usize] = r[a as usize] * r[b as usize]}));
    functions.insert("muli".to_string(), Box::new(|a: usize, b: usize, c: usize, r: &mut Vec<usize>|
        {r[c as usize] = r[a as usize] * b}));

    functions.insert("banr".to_string(), Box::new(|a: usize, b: usize, c: usize, r: &mut Vec<usize>|
        {r[c as usize] = r[a as usize] & r[b as usize]}));
    functions.insert("bani".to_string(), Box::new(|a: usize, b: usize, c: usize, r: &mut Vec<usize>|
        {r[c as usize] = r[a as usize] & b}));

    functions.insert("borr".to_string(), Box::new(|a: usize, b: usize, c: usize, r: &mut Vec<usize>|
        {r[c as usize] = r[a as usize] | r[b as usize]}));
    functions.insert("bori".to_string(), Box::new(|a: usize, b: usize, c: usize, r: &mut Vec<usize>|
        {r[c as usize] = r[a as usize] | b}));

    functions.insert("setr".to_string(), Box::new(|a: usize, _: usize, c: usize, r: &mut Vec<usize>|
        {r[c as usize] = r[a as usize]}));
    functions.insert("seti".to_string(), Box::new(|a: usize, _: usize, c: usize, r: &mut Vec<usize>|
        {r[c as usize] = a}));

    functions.insert("gtir".to_string(), Box::new(|a: usize, b: usize, c: usize, r: &mut Vec<usize>|
        {r[c as usize] = (a > r[b as usize]) as usize}));
    functions.insert("gtri".to_string(), Box::new(|a: usize, b: usize, c: usize, r: &mut Vec<usize>|
        {r[c as usize] = (r[a as usize] > b) as usize}));
    functions.insert("gtrr".to_string(), Box::new(|a: usize, b: usize, c: usize, r: &mut Vec<usize>|
        {r[c as usize] = (r[a as usize] > r[b as usize]) as usize}));

    functions.insert("eqir".to_string(), Box::new(|a: usize, b: usize, c: usize, r: &mut Vec<usize>|
        {r[c as usize] = (a == r[b as usize]) as usize}));
    functions.insert("eqri".to_string(), Box::new(|a: usize, b: usize, c: usize, r: &mut Vec<usize>|
        {r[c as usize] = (r[a as usize] == b) as usize}));
    functions.insert("eqrr".to_string(), Box::new(|a: usize, b: usize, c: usize, r: &mut Vec<usize>|
        {r[c as usize] = (r[a as usize] == r[b as usize]) as usize}));

    functions.insert("eqir".to_string(), Box::new(|a: usize, b: usize, c: usize, r: &mut Vec<usize>|
        {r[c as usize] = (a == r[b as usize]) as usize}));
    functions.insert("eqri".to_string(), Box::new(|a: usize, b: usize, c: usize, r: &mut Vec<usize>|
        {r[c as usize] = (r[a as usize] == b) as usize}));
    functions.insert("eqrr".to_string(), Box::new(|a: usize, b: usize, c: usize, r: &mut Vec<usize>|
        {r[c as usize] = (r[a as usize] == r[b as usize]) as usize}));
    return functions;
}

fn do_loop(r1: usize) -> usize {
    let mut total: usize = 0;
    for i in 1..=r1{
        if r1 % i == 0{
            total += i;
        }
    }
    return total;
}

pub fn solve() {
    let (ip, input) = parse_input();
    let mut reg: Vec<usize> = vec![0, 0, 0, 0, 0, 0];
    let functions = map_functions();

    while reg[ip as usize] < input.len() as usize{
        if reg[ip as usize] == 1{ break; }
        let (command, a, b, c) = &input[reg[ip as usize] as usize];
        functions.get(command.as_str()).unwrap()(*a, *b, *c, &mut reg);
        reg[ip as usize] += 1;
    }
    println!("First:  {}", do_loop(reg[1 as usize]));

    let mut reg: Vec<usize> = vec![1, 0, 0, 0, 0, 0];
    while reg[ip as usize] < input.len() as usize{
        if reg[ip as usize] == 1{ break; }
        let (command, a, b, c) = &input[reg[ip as usize] as usize];
        functions.get(command.as_str()).unwrap()(*a, *b, *c, &mut reg);
        reg[ip as usize] += 1;
    }
    println!("Second: {}", do_loop(reg[1 as usize]));
}
