use std::cmp::{max, min};
use std::collections::HashMap;
//Advent of Code 2021 day 23
use std::fs::File;
use std::io::{BufRead, BufReader};

fn parse_input() -> [[char; 2]; 4]{
    let filename = "AoC2021/solutions/23/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    let mut lines = Vec::<String>::new();
    let mut res= [[' '; 2]; 4];

    for line in reader.lines(){
        lines.push(line.unwrap());
    }

    res[0][0] = lines[2].chars().nth(3).unwrap();
    res[0][1] = lines[3].chars().nth(3).unwrap();

    res[1][0] = lines[2].chars().nth(5).unwrap();
    res[1][1] = lines[3].chars().nth(5).unwrap();

    res[2][0] = lines[2].chars().nth(7).unwrap();
    res[2][1] = lines[3].chars().nth(7).unwrap();

    res[3][0] = lines[2].chars().nth(9).unwrap();
    res[3][1] = lines[3].chars().nth(9).unwrap();

    return res;
}

#[derive(Hash, Debug, Copy, Clone)]
struct State{
    homes: [[char; 2]; 4],
    hallway: [char; 11],
}

impl State {
    fn new(homes: [[char; 2]; 4], hallway: [char; 11]) -> State{
        return State{homes, hallway};
    }

    fn new_init(homes: [[char; 2]; 4]) -> State{
        return State{homes, hallway: ['.'; 11]}
    }

    fn expand_into(&self, container: &mut Vec<(State, usize)>, weights: &HashMap<char, usize>){
        // Exit homes
        let home_start = 2;
        let home_dist = 2;
        let homes: [usize; 4] = [2, 4, 6, 8];

        for (i, home) in self.homes.iter().enumerate(){
            let expected_val = ((('A' as usize) + i) as u8) as char;
            if home.iter().all(|&c| c == '.' || c == expected_val){
                continue;
            }

            let mut selected = usize::MAX;
            for (j, &val) in home.iter().enumerate(){
                if val != '.' {
                    selected = j;
                    break;
                }
            }

            if selected != usize::MAX {
                let home_pos = home_start + i * home_dist;
                if self.hallway[home_pos-1] != '.' && self.hallway[home_pos + 1] != '.' { continue }

                let mut new_homes = self.homes;
                let mut new_hallway = self.hallway;
                let val = new_homes[i][selected];
                let weight = *weights.get(&val).unwrap();
                new_homes[i][selected] = '.';

                for i in 1..home_pos {
                    let pos = home_pos - i;
                    if self.hallway[pos] == '.' {
                        if homes.contains(&pos){ continue }
                        new_hallway[pos] = val;
                        container.push((State::new(new_homes, new_hallway), weight * (i + 1 + selected)));
                        new_hallway[pos] = '.';
                    }
                    else {
                        break;
                    }
                }

                for i in 1..(10 - home_pos) {
                    let pos = home_pos + i;
                    if self.hallway[pos] == '.' {
                        if homes.contains(&pos){ continue }
                        new_hallway[pos] = val;
                        container.push((State::new(new_homes, new_hallway), weight * (i + 1 + selected)));
                        new_hallway[pos] = '.';
                    }
                    else {
                        break;
                    }
                }
            }
        }

        let mut new_hallway = self.hallway;
        let mut new_homes = self.homes;
        // Try enter home
        for i in 0..=10{
            if self.hallway[i] == '.'{ continue }
            let val = self.hallway[i];
            let weight = *weights.get(&val).unwrap();
            let home_index = (val as usize) - ('A' as usize);
            let target_home = homes[home_index];

            // Check if the home contains only valid values
            let home_valid = self.homes[home_index].iter().all(|&c| c == val || c == '.');
            if !home_valid { continue }

            // Check if the path to home is free
            new_hallway[i] = '.';
            let path_valid = (min(i, target_home)..=max(i, target_home)).all(|j| new_hallway[j] == '.');
            if path_valid{
                let to_entry = ((i as i64) - (target_home as i64)).abs() as usize;
                let unoccupied = self.homes[home_index].iter().enumerate().rfind(|(_, &c)| c == '.').unwrap().0;
                new_homes[home_index][unoccupied] = val;
                let total_dist = to_entry + 1 + unoccupied;
                let total_weight = weight * total_dist;
                container.push((State::new(new_homes, new_hallway), total_weight));
                new_homes[home_index][unoccupied] = '.';
            }
            new_hallway[i] = val;
        }
    }

    fn is_winning(&self) -> bool{
        for (i, home) in self.homes.iter().enumerate(){
            let expected = ((('A' as usize) + i) as u8) as char;
            if !home.iter().all(|&c| c == expected) { return false }
        }
        return true;
    }
}


#[derive(Hash, Debug, Copy, Clone)]
struct AdvancedState{
    homes: [[char; 4]; 4],
    hallway: [char; 11],
}

impl AdvancedState {
    fn new(homes: [[char; 4]; 4], hallway: [char; 11]) -> AdvancedState{
        return AdvancedState{homes, hallway};
    }

    fn new_init(homes: [[char; 2]; 4]) -> AdvancedState{
        let mut new_homes = [[' '; 4]; 4];

        let folds = [  ['D', 'C', 'B', 'A'], ['D', 'B' ,'A' ,'C']];

        for i in 0..4{
            new_homes[i][0] = homes[i][0];
            new_homes[i][1] = folds[0][i];
            new_homes[i][2] = folds[1][i];
            new_homes[i][3] = homes[i][1];
        }

        return AdvancedState{homes: new_homes, hallway: ['.'; 11]}
    }

    fn expand_into(&self, container: &mut Vec<(AdvancedState, usize)>, weights: &HashMap<char, usize>){
        // Exit homes
        let home_start = 2;
        let home_dist = 2;
        let homes: [usize; 4] = [2, 4, 6, 8];

        for (i, home) in self.homes.iter().enumerate(){
            let expected_val = ((('A' as usize) + i) as u8) as char;
            if home.iter().all(|&c| c == '.' || c == expected_val){
                continue;
            }

            let mut selected = usize::MAX;
            for (j, &val) in home.iter().enumerate(){
                if val != '.' {
                    selected = j;
                    break;
                }
            }

            if selected != usize::MAX {
                let home_pos = home_start + i * home_dist;
                if self.hallway[home_pos-1] != '.' && self.hallway[home_pos + 1] != '.' { continue }

                let mut new_homes = self.homes;
                let mut new_hallway = self.hallway;
                let val = new_homes[i][selected];
                let weight = *weights.get(&val).unwrap();
                new_homes[i][selected] = '.';

                for i in 1..=home_pos {
                    let pos = home_pos - i;
                    if self.hallway[pos] == '.' {
                        if homes.contains(&pos){ continue }
                        new_hallway[pos] = val;
                        container.push((AdvancedState::new(new_homes, new_hallway), weight * (i + 1 + selected)));
                        new_hallway[pos] = '.';
                    }
                    else {
                        break;
                    }
                }

                for i in 1..=(10 - home_pos) {
                    let pos = home_pos + i;
                    if self.hallway[pos] == '.' {
                        if homes.contains(&pos){ continue }
                        new_hallway[pos] = val;
                        container.push((AdvancedState::new(new_homes, new_hallway), weight * (i + 1 + selected)));
                        new_hallway[pos] = '.';
                    }
                    else {
                        break;
                    }
                }
            }
        }

        let mut new_hallway = self.hallway;
        let mut new_homes = self.homes;
        // Try enter home
        for i in 0..=10{
            if self.hallway[i] == '.'{ continue }
            let val = self.hallway[i];
            let weight = *weights.get(&val).unwrap();
            let home_index = (val as usize) - ('A' as usize);
            let target_home = homes[home_index];

            // Check if the home contains only valid values
            let home_valid = self.homes[home_index].iter().all(|&c| c == val || c == '.');
            if !home_valid { continue }

            // Check if the path to home is free
            new_hallway[i] = '.';
            let path_valid = (min(i, target_home)..=max(i, target_home)).all(|j| new_hallway[j] == '.');
            if path_valid{
                let to_entry = ((i as i64) - (target_home as i64)).abs() as usize;
                let unoccupied = self.homes[home_index].iter().enumerate().rfind(|(_, &c)| c == '.').unwrap().0;
                new_homes[home_index][unoccupied] = val;
                let total_dist = to_entry + 1 + unoccupied;
                let total_weight = weight * total_dist;
                container.push((AdvancedState::new(new_homes, new_hallway), total_weight));
                new_homes[home_index][unoccupied] = '.';
            }
            new_hallway[i] = val;
        }
    }

    fn is_winning(&self) -> bool{
        for (i, home) in self.homes.iter().enumerate(){
            let expected = ((('A' as usize) + i) as u8) as char;
            if !home.iter().all(|&c| c == expected) { return false }
        }
        return true;
    }
}



fn first(){
    fn recurse(current_state: &State, current_score: usize, global_best: &mut usize, weights: &HashMap<char, usize>, stack: &mut Vec<(State, usize)>, solution_stack: &mut Vec<(State, usize)>){
        if current_score > *global_best{ return; }
        if current_state.is_winning(){
            if current_score < *global_best{
                *global_best = current_score;
            }
            return;
        }

        let stack_len = stack.len();
        current_state.expand_into(stack, weights);

        while stack.len() > stack_len {
            let (state, weight) = stack.pop().unwrap();

            solution_stack.push((state.clone(), current_score + weight));
            recurse(&state, current_score + weight, global_best, weights, stack, solution_stack);
            solution_stack.pop();
        }
    }


    let input = parse_input();
    let init_state = State::new_init(input);
    let weights:  HashMap<char, usize> = HashMap::from([('A', 1), ('B', 10), ('C', 100), ('D', 1000)]);
    let mut stack: Vec<(State, usize)> = Vec::new();
    let mut best_score = usize::MAX;
    let mut solution_stack = Vec::<(State, usize)>::new();

    recurse(&init_state, 0, &mut best_score, &weights, &mut stack, &mut solution_stack);

    println!("First:  {}", best_score);
}

fn second(){
    fn recurse(current_state: &AdvancedState, current_score: usize, global_best: &mut usize, weights: &HashMap<char, usize>, stack: &mut Vec<(AdvancedState, usize)>, solution_stack: &mut Vec<(AdvancedState, usize)>){
        if current_score > *global_best{ return; }
        if current_state.is_winning(){
            if current_score < *global_best{
                *global_best = current_score;
            }
            return;
        }

        let stack_len = stack.len();
        current_state.expand_into(stack, weights);
        stack[stack_len..].sort_by(|(_, a), (_, b)| a.cmp(b));

        while stack.len() > stack_len {
            let (state, weight) = stack.pop().unwrap();

            solution_stack.push((state.clone(), current_score + weight));
            recurse(&state, current_score + weight, global_best, weights, stack, solution_stack);
            solution_stack.pop();
        }
    }


    let input = parse_input();
    let init_state = AdvancedState::new_init(input);
    let weights:  HashMap<char, usize> = HashMap::from([('A', 1), ('B', 10), ('C', 100), ('D', 1000)]);
    let mut stack: Vec<(AdvancedState, usize)> = Vec::new();
    let mut best_score = usize::MAX;
    let mut solution_stack = Vec::<(AdvancedState, usize)>::new();

    recurse(&init_state, 0, &mut best_score, &weights, &mut stack, &mut solution_stack);

    println!("Second: {}", best_score);
}

pub fn solve() {
    first();
    second();
}
