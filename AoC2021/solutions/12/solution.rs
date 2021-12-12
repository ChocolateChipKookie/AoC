use std::collections::HashSet;
//Advent of Code 2021 day 12
use std::fs::File;
use std::io::{BufRead, BufReader};

fn parse_input() -> Vec<(String, String)>{
    let filename = "AoC2021/solutions/12/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    let mut inputs: Vec<(String, String)> = Vec::new();

    for line_i in reader.lines(){
        let line = line_i.unwrap();
        let mut tokens = line.split("-");
        let start = tokens.next().unwrap();
        let end = tokens.next().unwrap();
        inputs.push((start.to_string(), end.to_string()));
        inputs.push((end.to_string(), start.to_string()));
    }

    return inputs;
}

fn recurse(links: &Vec<(String, String)>, node: &str, visited: &mut HashSet<String>, extra: i32) -> i32 {
    if node == "end"{
        return 1;
    }
    let is_big = node.chars().next().unwrap().is_uppercase();
    let insert_visited = !is_big && !visited.contains(node);
    if insert_visited { visited.insert(node.to_string()); }

    let mut total = 0;
    for (start, end) in links.iter() {
        if start.to_string() != node { continue }
        if visited.contains(&end.to_string()) {
            if extra > 0 && end != "start" {
                total += recurse(links, end, visited, extra - 1);
            }
            continue;
        }
        total += recurse(links, end, visited, extra);
    }

    if insert_visited { visited.remove(node); }
    return total;
}

fn count_paths(extra_visits: i32) -> i32{
    let links = parse_input();
    return recurse(&links, "start", &mut HashSet::new(), extra_visits);
}

pub fn solve() {
    println!("First:  {}", count_paths(0));
    println!("Second: {}", count_paths(1));
}
