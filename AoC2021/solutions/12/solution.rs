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

fn count_paths(extra_visits: i32) -> i32{
    let links = parse_input();
    let mut distinct_paths = 0;
    let mut state: Vec<(String, HashSet<String>, i32)> = Vec::new();
    state.push(("start".to_string(), HashSet::new(), extra_visits));

    while state.len() > 0 {
        let (node, visited, extra) = state.pop().unwrap();

        if node == "end" {
            distinct_paths += 1;
            continue;
        }

        let is_big = node.chars().next().unwrap().is_uppercase();

        for (start, end) in links.iter(){
            if start.to_string() != node {continue}
            let was_visited = visited.contains(&end.to_string());
            let mut next_extra = extra;
            if was_visited{
                if extra > 0 && end != "start"{
                    next_extra -= 1;
                }
                else {
                    continue;
                }
            }

            let mut new_visited = visited.clone();
            if ! is_big{
                new_visited.insert(node.to_string());
            }
            state.push((end.to_string(), new_visited, next_extra));
        }
    }
    return distinct_paths;
}

pub fn solve() {
    println!("First:  {}", count_paths(0));
    println!("Second: {}", count_paths(1));
}
