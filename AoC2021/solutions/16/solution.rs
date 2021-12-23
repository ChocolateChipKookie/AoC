use std::collections::HashMap;
//Advent of Code 2021 day 16
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::sync::atomic::{AtomicUsize, Ordering};

fn parse_input() -> Vec<char>{
    let filename = "AoC2021/solutions/16/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    return reader.lines().next().unwrap().unwrap().chars().collect();
}

fn to_bin(hex_i: &Vec<char>) -> Vec<bool>{
    let map: HashMap<char, i32> = HashMap::from_iter("0123456789ABCDEF".chars().enumerate().map(|(i, c)| (c, i as i32)));
    let hex: Vec<i32> = hex_i.iter().map(|c| *map.get(c).unwrap()).collect();

    let mut res: Vec<bool> = Vec::with_capacity(hex.len() * 4);
    for val in hex{
        for pos in 0..4{
            res.push((val & (1 << (3 - pos))) != 0);
        }
    }

    return res;
}

fn to_int(bin: &[bool]) -> usize{
    let mut res = 0;
    let mut multiplier = 1;
    for &b in bin.iter().rev(){
        if b{
            res += multiplier;
        }
        multiplier *= 2;
    }
    return res;
}

fn get_id() -> usize {
    static COUNTER: AtomicUsize = AtomicUsize::new(0);
    return COUNTER.fetch_add(1, Ordering::Relaxed);
}

struct Packet {
    version: usize,
    type_id: usize,
    value: usize,
    id: usize,
    parent: usize
}

impl Packet {
    fn new_packet(version: usize, type_id: usize, parent: usize) -> Packet{
        return Packet{version, type_id, value: 0, id: get_id(), parent};
    }

    fn new_literal(version: usize, value: usize, parent: usize) -> Packet{
        return Packet{version, type_id: 4, value, id: get_id(), parent};
    }
}

fn parse(mut p: usize, data: &[bool], packets: &mut Vec<Packet>, parent: usize) -> usize{
    let version = to_int(&data[p..(p+3)]);
    p += 3;
    let type_id = to_int(&data[p..(p+3)]);
    p += 3;

    if type_id == 4 {
        let mut value: usize = 0;
        loop {
            value *= 16;
            value += to_int(&data[(p+1)..(p+5)]);
            if !data[p]{ break }
            p += 5;
        }
        p += 5;
        packets.push(Packet::new_literal(version, value, parent));
    }
    else{
        let length_id: usize = if data[p] {1} else {0};
        if length_id == 0{
            let length = to_int(&data[(p + 1)..(p + 16)]);
            p += 16;
            let segment_end = p + length;
            let this = Packet::new_packet(version, type_id, parent);
            let id = this.id;
            packets.push(this);

            while p < segment_end{
                p = parse(p, data, packets, id);
            }
        } else {
            let  length = to_int(&data[(p + 1)..(p + 12)]);
            p += 12;
            let this = Packet::new_packet(version, type_id, parent);
            let id = this.id;
            packets.push(this);

            for _ in 0..length{
                p = parse(p, data, packets, id);
            }
        }
    }

    return p;
}

fn walk(id: usize, packets: &Vec<Packet>) -> usize {
    let this = packets.iter().find(|p| p.id == id).unwrap();
    if this.type_id == 4 {
        return this.value;
    }
    let mut values = packets
        .iter()
        .filter(|p| p.parent == id)
        .map(|p| walk(p.id, packets));

    match this.type_id {
        0 => return values.sum(),
        1 => return values.fold(1 as usize, |acc, i| acc * i),
        2 => return values.min().unwrap(),
        3 => return values.max().unwrap(),
        5 => return if values.next().unwrap() >  values.next().unwrap() {1} else {0},
        6 => return if values.next().unwrap() <  values.next().unwrap() {1} else {0},
        7 => return if values.next().unwrap() == values.next().unwrap() {1} else {0},
        _ => panic!("AA")
    }
}



pub fn solve() {
    let input = parse_input();
    let data = to_bin(&input);

    let mut packets = Vec::new();
    parse(0, &data[..], &mut packets, usize::MAX);

    println!("First:  {}", packets.iter().map(|p| p.version).sum::<usize>());
    println!("Second: {}", walk(packets[0].id, &packets));
}
