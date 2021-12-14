use std::collections::HashMap;
//Advent of Code 2018 day 20
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::str::Chars;

fn parse_input() -> String{
    let filename = "AoC2018/solutions/20/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    return reader.lines().next().unwrap().unwrap();
}

fn recurse(mut pos: (i32, i32), directions: & HashMap<char, (i32, i32)>, known: &mut Vec<((i32, i32), char)>, stream: &mut Chars) -> bool{
    loop {
        let c_o = stream.next();
        if c_o.is_none() || c_o.unwrap() == '$'{
            return false;
        }

        let c = c_o.unwrap();
        if directions.contains_key(&c){
            let d = directions.get(&c).unwrap();
            pos.0 +=  d.0;
            pos.1 +=  d.1;
            known.push((*pos, 'x'));
            pos.0 +=  d.0;
            pos.1 +=  d.1;
            known.push((*pos, '.'));
        }
        else {
            match c {
                '(' => print!("("),
                ')' => print!(")"),
                '|' => print!("|"),
                _ => panic!("WTF")
            }
        }

    }




    return true;
}

fn expand_map(regex: String){
    let mut char_iter = regex.chars();
    let mut known = Vec::from([((0, 0), '.')]);
    let directions = HashMap::from([
        ('N', ( 0, -1)),
        ('S', ( 0,  1)),
        ('W', (-1,  0)),
        ('E', ( 1,  0)),
    ]);
    recurse((0, 0), &directions, &mut known, &mut char_iter);
}

pub fn solve() {
    let input = parse_input();
    println!("{}", input);


    let first  = 0;
    let second = 0;
    println!("First:  {}", first);
    println!("Second: {}", second);
}
