#[path = "../AoC2023/solutions/02/solution.rs"] mod solution;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    solution::solve();
    println!("Time elapsed: {}us", now.elapsed().as_micros());
}