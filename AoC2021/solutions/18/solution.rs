//Advent of Code 2021 day 18
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::cmp::max;

struct Node{
    left: usize,
    right: usize,
    parent: usize,
    value: usize
}

impl Node {
    fn new(parent: usize) -> Node{
        return Node{left: 0, right: 0, parent, value: 0};
    }
    fn new_value(parent: usize, value: usize) -> Node{
        return Node{left: 0, right: 0, parent, value};
    }
}

fn parse(val: &str, parent: usize, nodes: &mut Vec<Node>) -> usize{
    fn find_split(val: &str) -> usize{
        let mut count: usize = 0;
        for (i, c) in val.chars().enumerate(){
            match c {
                '[' => count += 1,
                ']' => count -= 1,
                ',' => if count == 1 {return i},
                _   => {}
            }
        }
        return usize::MAX;
    }
    let id = nodes.len();
    nodes.push(Node::new(parent));

    let split = find_split(val);
    if split != usize::MAX{
        nodes[id].left = parse(&val[1..split], id, nodes);
        nodes[id].right = parse(&val[(split + 1)..(val.len() - 1)], id, nodes);
    } else {
        nodes[id].value = val.parse::<usize>().unwrap();
    }

    return id;
}

fn parse_input() -> Vec<Vec<Node>>{
    let filename = "AoC2021/solutions/18/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    let mut inputs: Vec<Vec<Node>> = Vec::new();

    for line in reader.lines(){
        let mut nodes: Vec<Node> = Vec::new();
        parse(line.unwrap().as_str(), usize::MAX, &mut nodes);
        inputs.push(nodes);
    }

    return inputs;
}

fn reduce(nodes: &mut Vec<Node>) {
    fn explode(nodes: &mut Vec<Node>)->bool{
        fn find_to_explode(node: usize, depth: usize, nodes: &Vec<Node>) -> usize{
            if nodes[node].left == 0 { return 0 };
            if depth >= 4 { return node };

            let left = find_to_explode(nodes[node].left, depth + 1, nodes);
            if left != 0 { return left };
            let right = find_to_explode(nodes[node].right, depth + 1, nodes);
            if right != 0 { return right };
            return 0;
        }

        let to_explode = find_to_explode(0, 0, nodes);
        if to_explode == 0 {return false};
        let mut parent = nodes[to_explode].parent;
        let mut current = to_explode;

        while parent != usize::MAX && nodes[parent].left == current{
            current = parent;
            parent = nodes[parent].parent;
        }
        if parent != usize::MAX{
            current = nodes[parent].left;
            while nodes[current].right != 0{
                current = nodes[current].right;
            }
            nodes[current].value += nodes[nodes[to_explode].left].value;
        }

        let mut parent = nodes[to_explode].parent;
        let mut current = to_explode;

        while parent != usize::MAX && nodes[parent].right == current {
            current = parent;
            parent = nodes[parent].parent;
        }
        if parent != usize::MAX{
            current = nodes[parent].right;
            while nodes[current].left != 0{
                current = nodes[current].left;
            }
            nodes[current].value += nodes[nodes[to_explode].right].value;
        }
        nodes[to_explode].left = 0;
        nodes[to_explode].right = 0;
        nodes[to_explode].value = 0;
        return true;
    }

    fn split(nodes: &mut Vec<Node>)->bool{
        fn find_to_split(node: usize, nodes: &Vec<Node>) -> usize{
            if nodes[node].value >= 10 { return node };
            if nodes[node].left == 0 {return 0};
            let left = find_to_split(nodes[node].left, nodes);
            if left != 0 { return left };
            let right = find_to_split(nodes[node].right, nodes);
            if right != 0 { return right };
            return 0;
        }

        let to_split = find_to_split(0, nodes);
        if to_split == 0 { return false };

        let value = nodes[to_split].value;

        nodes[to_split].left = nodes.len();
        nodes.push(Node::new_value(to_split, ((value as f64) / 2.).floor() as usize));
        nodes[to_split].right = nodes.len();
        nodes.push(Node::new_value(to_split, ((value as f64) / 2.).ceil() as usize));
        nodes[to_split].value = 0;
        return true;
    }

    loop {
        if explode(nodes) {continue};
        if split(nodes) {continue};
        break;
    }
}

fn combine(left: &Vec<Node>, right: &Vec<Node>) -> Vec<Node>{
    let mut nodes: Vec<Node> = Vec::new();
    let mut root = Node::new(usize::MAX);

    let offset_left = 1;
    let offset_right = left.len() + 1;
    root.left = offset_left;
    root.right = offset_right;

    nodes.push(root);

    for node in left{
        let parent = if node.parent == usize::MAX {0} else {node.parent + offset_left};
        let mut successor = Node::new(parent);
        if node.left == 0 && node.right == 0 {
            successor.value = node.value;
        } else{
            successor.left = node.left + offset_left;
            successor.right = node.right + offset_left;
        }
        nodes.push(successor);
    }

    for node in right{
        let parent = if node.parent == usize::MAX {0} else {node.parent + offset_right};
        let mut successor = Node::new(parent);
        if node.left == 0 && node.right == 0 {
            successor.value = node.value;
        } else{
            successor.left = node.left + offset_right;
            successor.right = node.right + offset_right;
        }
        nodes.push(successor);
    }

    return nodes;
}

fn add(left: &Vec<Node>, right: &Vec<Node>) -> Vec<Node>{
    let mut c = combine(left, right);
    reduce(&mut c);
    return c;
}

fn magnitude(node: usize, nodes: &Vec<Node>) -> usize{
    if nodes[node].left == 0 {
        return nodes[node].value;
    }
    return magnitude(nodes[node].left, nodes) * 3 + magnitude(nodes[node].right, nodes) * 2
}

fn first(){
    let input: Vec<Vec<Node>> = parse_input();
    let mut sum = add(&input[0], &input[1]);
    for nodes in &input[2..]{
        sum = add(&sum, nodes);
    }

    println!("First:  {}", magnitude(0, &sum));
}

fn second(){
    let input: Vec<Vec<Node>> = parse_input();
    let mut res: usize = 0;
    for i1 in 0..input.len(){
        for i2 in 0..input.len() {
            let sum = add(&input[i1], &input[i2]);
            res = max(res, magnitude(0, &sum));
        }
    }

    println!("First:  {}", res);
}

pub fn solve() {
    first();
    second();
}
