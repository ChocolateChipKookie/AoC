//Advent of Code 2021 day 15
use std::fs::File;
use std::io::{BufRead, BufReader};

fn parse_input() -> Vec<Vec<usize>>{
    let filename = "AoC2021/solutions/15/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    return reader
        .lines()
        .map(|l| l
            .unwrap()
            .chars()
            .map(|c| c.to_digit(10).unwrap() as usize)
            .collect())
        .collect();
}

fn find_path(map: &Vec<Vec<usize>>) -> usize {
    let mut open: Vec<(usize, usize, usize, usize)> = Vec::new();
    let mut closed: Vec<(usize, usize, usize)> = Vec::new();
    let dims = (map[0].len() as i32, map.len() as i32);
    let end = (dims.0 - 1, dims.1 - 1);

    open.push((0, 0, 0, 0));
    let directions: [(i32, i32); 4] = [(0, -1), (1, 0), (0, 1), (-1, 0)];

    let heuristic = |x: i32, y: i32| ((end.0 - x).abs() + (end.1 - y).abs()) as usize;

    while open.len() > 0 {
        let (i, min_ele) = open.iter().enumerate().min_by_key(|(_, n)| n.2 + n.3).unwrap();
        let (x, y, cost, h) = *min_ele;
        open.remove(i);

        for (dx, dy) in directions{
            let ix = (x as i32) + dx;
            let iy = (y as i32) + dy;

            if ix < 0 || dims.0 <= ix || iy < 0 || dims.1 <= iy{
                continue
            }

            let nx = ix as usize;
            let ny = iy as usize;

            if (ix, iy) == end {
                return cost + map[ny][nx];
            }

            let n_cost = cost + map[ny][nx];
            let n_heuristic = heuristic(ix, iy);
            let n_priority = n_cost + n_heuristic;

            if open.iter().find(|&&n| n.0 == nx && n.1 == ny && (n.2 + n.3) <= n_priority).is_some(){
                continue;
            }
            if closed.iter().find(|&&n| n.0 == nx && n.1 == ny && n.2 <= n_priority).is_some(){
                continue;
            }
            open.push((nx, ny, n_cost, n_heuristic));
        }
        closed.push((x, y, cost + h));
    }
    return 0;
}

pub fn solve() {
    let small_map = parse_input();
    println!("First:  {}", find_path(&small_map));

    let dims = (small_map[0].len(), small_map.len());
    let repeats: usize = 5;
    let mut big_map: Vec<Vec<usize>> = vec![vec![0; dims.0 * 5]; dims.1 * 5];

    for yi in 0..repeats{
        let y0 = yi * dims.1;
        for xi in 0..repeats{
            let x0 = xi * dims.0;
            let risk = xi + yi;

            for y in 0..dims.1{
                for x in 0..dims.0{
                    big_map[y + y0][x + x0] = (small_map[y][x] - 1 + risk) % 9 + 1;
                }
            }
        }
    }

    println!("Second: {}", find_path(&big_map));
}
