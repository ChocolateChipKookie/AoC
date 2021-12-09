#[path = "../AoC2021/solutions/09/solution.rs"] mod solution;

fn main() {
    let now = Instant::now();
    solution::solve();
    println!("Time elapsed: {}us", now.elapsed().as_micros());
}