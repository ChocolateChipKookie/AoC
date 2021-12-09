//Advent of Code 2018 day 17
use std::fs::File;
use std::io::{BufRead, BufReader};

fn print_map(map: &Vec::<Vec::<char>>){
    for line in map{
        for c in line {
            print!("{}", c);
        }
        print!("\n");
    }
}

fn parse_input() -> (Vec::<Vec::<char>>, usize, usize, usize){
    let filename = "AoC2018/solutions/17/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    let mut clay = Vec::<(usize, usize)>::with_capacity(1000);

    for it in reader.lines(){
        let line = it.unwrap();
        let tokens:   Vec<Vec<&str>> = line.split(", ").map(|x| x.split("=").collect()).collect();

        let parallel = &tokens[0];
        let perpendicular = &tokens[1];

        if parallel[0] == "x"{
            let x: usize = parallel[1].parse().unwrap();
            let range: Vec<usize> = perpendicular[1].split("..").map(|r| r.parse::<usize>().unwrap()).collect();

            for y in range[0]..=range[1]{
                clay.push((x, y));
            }
        }
        else{
            let y: usize = parallel[1].parse().unwrap();
            let range: Vec<usize> = perpendicular[1].split("..").map(|r| r.parse::<usize>().unwrap()).collect();

            for x in range[0]..=range[1]{
                clay.push((x, y));
            }
        }
    }

    let min_x = clay.iter().map(|c| c.0).min().unwrap();
    let max_x = clay.iter().map(|c| c.0).max().unwrap();
    let min_y = clay.iter().map(|c| c.1).min().unwrap();
    let max_y = clay.iter().map(|c| c.1).max().unwrap();

    let width  = max_x - min_x + 3;
    let height = max_y + 1 - min_y;
    let offset_x = min_x - 1;
    let offset_y = min_y;

    let mut res: Vec<Vec<char>> = vec![vec![' '; width]; height]; 

    for (x, y) in clay{
        res[y - offset_y][x - offset_x] = '#';
    }
    return (res, height, width, 500 - offset_x);
}

#[derive(Debug)]
    struct Node{
        prev: usize,
        id: usize,
        x: usize,
        y: usize,
        drained: bool,
        child_stuck: bool
    }

pub fn solve() {
    

    let (mut map, height, width, start) = parse_input();

    let mut nodes = Vec::<Node>::new();
    let mut call_stack = Vec::<usize>::new();

    fn find_node(nodes: &Vec<Node>, x: usize, y: usize) -> usize {
        let node =  nodes.iter().find(|n| n.x == x && n.y == y);
        return node.unwrap().id;
    }

    fn add_node(nodes: &mut Vec<Node>, call_stack: &mut Vec<usize>, prev: usize, x: usize, y: usize) -> usize{
        let id = nodes.len();
        nodes.push(Node{prev, id, x, y, drained: false, child_stuck: false});
        call_stack.push(id);
        return id;
    }
    fn recursive_drain(nodes: &mut Vec<Node>, id: usize){
        let mut current: usize = id;

        while current != usize::MAX {
            if nodes[current].drained{
                break;
            }
            nodes[current].drained = true;
            current = nodes[current].prev;
        }
    }

    add_node(&mut nodes, &mut call_stack, usize::MAX, start, 0);
    
    while !call_stack.is_empty(){
        let id: usize = *call_stack.last().unwrap();
        if nodes[id].drained{
            call_stack.pop();
            continue;
        }

        let pos: (usize, usize) = (nodes[id].x, nodes[id].y);

        map[pos.1][pos.0] = '~';
        if pos.1 + 1 == height{
            recursive_drain(&mut nodes, id);
            call_stack.pop();
            continue;
        }
        if map[pos.1 + 1][pos.0] == ' '{
            let child = add_node(&mut nodes, &mut call_stack, id, pos.0, pos.1 + 1);
            call_stack.push(child);
            continue;
        }
        if map[pos.1 + 1][pos.0] == '~'{
            let node_under = find_node(&nodes, pos.0, pos.1 + 1);
            if nodes[node_under].drained{
                call_stack.pop();
                recursive_drain(&mut nodes, id);
                continue;
            }
        }

        let mut stuck = true;
        if map[pos.1][pos.0 - 1] == ' '{
            let child = add_node(&mut nodes, &mut call_stack, id, pos.0 - 1, pos.1);
            call_stack.push(child);
            stuck = false;
        }
        else if map[pos.1][pos.0 - 1] == '~'{
            let node_left = find_node(&nodes, pos.0 - 1, pos.1);
            if nodes[node_left].drained{
                call_stack.pop();
                recursive_drain(&mut nodes, id);
                stuck = false;
            }
        }
        if map[pos.1][pos.0 + 1] == ' '{
            let child = add_node(&mut nodes, &mut call_stack, id, pos.0 + 1, pos.1);
            call_stack.push(child);
            stuck = false;
        }
        else if map[pos.1][pos.0 + 1] == '~'{
            let node_right = find_node(&nodes, pos.0 + 1, pos.1);
            if nodes[node_right].drained{
                call_stack.pop();
                recursive_drain(&mut nodes, id);
                stuck = false;
            }
        }

        if stuck{
            call_stack.pop();
            let parent = nodes[id].prev;
            nodes[parent].child_stuck = true;
        }
    }

    let mut to_drain = Vec::<(usize, usize)>::new();
    for x in 0..width{
        if map[height - 1][x] == '~'{
            to_drain.push((x, height-1));
        }
    }

    while !to_drain.is_empty(){
        let (x, y) = to_drain.pop().unwrap();
        map[y][x] = '|';
        if x > 0 && map[y][x - 1] == '~'{
            to_drain.push((x - 1, y));
        }
        if x < width - 1 && map[y][x + 1] == '~'{
            to_drain.push((x + 1, y));
        }
        if y > 0 && map[y - 1][x] == '~'{
            to_drain.push((x, y - 1));
        }
    }

    print_map(&map);
    let second: usize = map.iter().map(|r| r.iter().filter(|&c| *c == '~').count()).sum();
    println!("First:  {}", nodes.len());
    println!("Second: {}", second);
}
