//Advent of Code 2018 day 21
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::collections::{HashMap, HashSet};

fn parse_input() -> (usize, Vec::<(String, usize, usize, usize)>){
    let filename = "AoC2018/solutions/21/input";
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

pub fn solve() {
    let (ip, input) = parse_input();
    let mut reg: Vec<usize> = vec![0, 0, 0, 0, 0, 0];
    let functions = map_functions();

    while reg[ip as usize] < input.len() as usize{
        if reg[ip as usize] == 28 {
            break;
        }
        let (command, a, b, c) = &input[reg[ip as usize] as usize];
        functions.get(command.as_str()).unwrap()(*a, *b, *c, &mut reg);
        reg[ip as usize] += 1;
    }

    println!("First:  {}", reg[2 as usize]);

    let mut r1: usize = 65536;
    let mut r2: usize = 1250634;

    let mut visited: HashSet<usize> = HashSet::new();
    let mut last: usize = 0;
    loop {
        r2 += r1 & 255;
        r2 &= 16777215;
        r2 *= 65899;
        r2 &= 16777215;
        if r1 < 256 {
            if visited.contains(&r2){
                break;
            }
            last = r2;
            visited.insert(r2);
            r1 = r2 | 65536;
            r2 = 1250634;
        }
        else{
            r1 /= 256;
        }
    }
    print!("Second: {}\n", last);
}
