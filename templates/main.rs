#[path = "../AoC{year}/solutions/{filled}/solution.rs"] mod solution;
use std::time::Instant;

fn main() {{
    let now = Instant::now();
    solution::solve();
    println!("Time elapsed: {{}}us", now.elapsed().as_micros());
}}