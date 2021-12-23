use std::cmp::max;
//Advent of Code 2021 day 19
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::mem::swap;
use rand::seq::SliceRandom;

fn parse_input() -> Vec<Vec<(i64, i64, i64)>>{
    let filename = "AoC2021/solutions/19/input";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    let mut scanners: Vec<Vec<(i64, i64, i64)>> = Vec::new();

    let mut beacons: Vec<(i64, i64, i64)> = Vec::new();

    for line_i in reader.lines(){
        let line = line_i.unwrap();
        if line.starts_with("---") { continue };
        if line.len() == 0{
            scanners.push(beacons.clone());
            beacons.clear();
            continue;
        }
        let mut ns = line.split(",").map(|v| v.parse::<i64>().unwrap());
        beacons.push((ns.next().unwrap(), ns.next().unwrap(), ns.next().unwrap()))
    }
    scanners.push(beacons.clone());

    return scanners;
}

fn rotate_xy(p: &(i64, i64, i64)) -> (i64, i64, i64){
    return (p.1, -p.0, p.2);
}
fn rotate_xz(p: &(i64, i64, i64)) -> (i64, i64, i64){
    return (p.2, p.1, -p.0);
}
fn rotate_yz(p: &(i64, i64, i64)) -> (i64, i64, i64){
    return (p.0, p.2, -p.1);
}

fn rotate(mut p: (i64, i64, i64), rotation: &(usize, usize, usize)) -> (i64, i64, i64){
    for _ in 0..rotation.0{
        p = rotate_xy(&p);
    }
    for _ in 0..rotation.1{
        p = rotate_xz(&p);
    }
    for _ in 0..rotation.2{
        p = rotate_yz(&p);
    }
    return p;
}

fn inverse_rotate(mut p: (i64, i64, i64), rotation: &(usize, usize, usize)) -> (i64, i64, i64){
    for _ in 0..(4 - rotation.2){
        p = rotate_yz(&p);
    }
    for _ in 0..(4 - rotation.1){
        p = rotate_xz(&p);
    }
    for _ in 0..(4 - rotation.0){
        p = rotate_xy(&p);
    }
    return p;
}

fn transform(mut p: (i64, i64, i64), rotation: &(usize, usize, usize), translation:  &(i64, i64, i64)) -> (i64, i64, i64){
    p = rotate(p, rotation);
    p.0 += translation.0;
    p.1 += translation.1;
    p.2 += translation.2;
    return p;
}

fn inverse_transform(mut p: (i64, i64, i64), rotation: &(usize, usize, usize), translation:  &(i64, i64, i64)) -> (i64, i64, i64){
    p.0 -= translation.0;
    p.1 -= translation.1;
    p.2 -= translation.2;
    p = inverse_rotate(p, rotation);
    return p;
}

fn match_pos(target_i: usize, all: &Vec<Vec<(i64, i64, i64)>>, groups: &Vec<Vec<usize>>) -> Option<(usize, usize, (usize, usize, usize), (i64, i64, i64))>{
    fn pair_hash(p0: &(i64, i64, i64), p1: &(i64, i64, i64)) -> i64{
        return (p0.0 - p1.0).abs() + (p0.1 - p1.1).abs() + (p0.2 - p1.2).abs();
    }

    fn spatial_hash(points: &Vec<(i64, i64, i64)>) -> i64{
        let mut total: i64 = 0;
        for i0 in 0..points.len(){
            for i1 in (i0 + 1)..points.len(){
                total += pair_hash(&points[i0], &points[i1]);
            }
        }
        return total;
    }

    fn test_transform(target: &Vec<(i64, i64, i64)>, points: &Vec<(i64, i64, i64)>, rotation: (usize, usize, usize), translation: (i64, i64, i64)) -> bool {
        for point in points.iter(){
            let pt = transform(*point, &rotation, &translation);
            if !target.contains(&pt) {
                return false;
            }
        }
        return true;
    }

    let mut rng = rand::thread_rng();

    let reference_points_needed = 12;
    let match_target = &all[target_i];
    let group = groups.iter().find(|g| g.contains(&target_i)).unwrap();

    let mut rotations: Vec<(usize, usize, usize)> = Vec::new();
    (0..4).for_each(|i| rotations.push((i, 0, 0)));
    (0..4).for_each(|i| rotations.push((i, 1, 0)));
    (0..4).for_each(|i| rotations.push((i, 2, 0)));
    (0..4).for_each(|i| rotations.push((i, 3, 0)));
    (0..4).for_each(|i| rotations.push((i, 1, 1)));
    (0..4).for_each(|i| rotations.push((i, 1, 3)));

    for (match_i, match_source_) in all.iter().enumerate(){
        if group.contains(&match_i) { continue };

        let mut match_source = match_source_.clone();
        match_source.shuffle(&mut rng);

        let mut source_points: Vec<(i64, i64, i64)> = Vec::new();
        source_points.push(match_source.pop().unwrap());
        source_points.push(match_source.pop().unwrap());
        let ref_hash = pair_hash(&source_points[0], &source_points[1]);

        let mut target_points: Vec<(i64, i64, i64)> = Vec::new();
        let current_len = match_target.len();
        let mut found = false;

        'hash_loop:
        for i0 in 0..current_len{
            for i1 in 0..current_len{
                let hash = pair_hash(&match_target[i0], &match_target[i1]);
                if hash == ref_hash{
                    target_points.push(match_target[i0]);
                    target_points.push(match_target[i1]);
                    found = true;
                    break 'hash_loop
                }
            }
        }
        if !found { continue }

        while found && source_points.len() < reference_points_needed {
            found = false;
            'search_loop:
            for p_source in match_source.iter(){
                if source_points.contains(p_source){ continue }
                source_points.push(*p_source);

                for p_target in match_target.iter(){
                    target_points.push(*p_target);
                    if spatial_hash(&source_points) == spatial_hash(&target_points) {
                        found = true;
                        break 'search_loop
                    }
                    target_points.pop();
                }

                source_points.pop();
            }
        }

        if !found{ continue; }

        let mut translation: (i64, i64, i64) = (0, 0, 0);
        let mut rotation: (usize, usize, usize) = (0, 0, 0);

        found = false;
        'match_loop:
        for target_point_i in 0..target_points.len(){
            let target_point = target_points[target_point_i];

            for source_point_i in 0..source_points.len(){
                let source_point = source_points[source_point_i];

                for r in rotations.iter(){
                    let rotated = rotate(source_point, r);
                    translation.0 = target_point.0 - rotated.0;
                    translation.1 = target_point.1 - rotated.1;
                    translation.2 = target_point.2 - rotated.2;

                    if test_transform(match_target, &source_points, *r, translation){
                        rotation = *r;
                        found = true;
                        break 'match_loop
                    }
                }
            }
        }
        if !found {continue};
        return Some((target_i, match_i, rotation, translation));
    }
    return None;
}

fn stitch_cloud(matches:& Vec<(usize, usize, (usize, usize, usize), (i64, i64, i64))>, all: &Vec<Vec<(i64, i64, i64)>>) -> Vec<(i64, i64, i64)>{
    let mut res = all.clone();
    let mut links = vec![usize::MAX; all.len()];
    links[0] = 0;
    loop{
        if links.iter().find(|&&i| i == usize::MAX).is_none(){
            break;
        }
        for m in matches.iter(){
            if links[m.0] != usize::MAX{
                if links[m.1] == usize::MAX{
                    links[m.1] = m.0;
                }
            }

            if links[m.1] != usize::MAX{
                if links[m.0] == usize::MAX {
                    links[m.0] = m.1
                }
            }
        }
    }
    links[0] = usize::MAX;

    let mut running = true;

    while running {
        running = false;

        for &m in matches.iter(){
            let (mut target_i, mut match_i, rotation, translation) = m;
            let mut inverse = false;
            if links[match_i] != target_i{
                swap(&mut target_i, &mut match_i);
                inverse = true;
            }
            if links[match_i] != target_i{
                continue;
            }
            if res[match_i].is_empty(){
                continue;
            }
            running = true;

            let match_points = res[match_i].clone();
            res[match_i].clear();
            let target_points = &mut res[target_i];
            for &point in match_points.iter(){
                let transformed;
                if inverse{
                    transformed = inverse_transform(point, &rotation, &translation);
                }
                else{
                    transformed = transform(point, &rotation, &translation);
                }
                if !target_points.contains(&transformed){
                    target_points.push(transformed);
                }
            }
        }
    }

    return res[0].clone();
}

pub fn solve() {
    let mut all = parse_input();

    // Reference, the map, transform
    let mut map_matches: Vec<(usize, usize, (usize, usize, usize), (i64, i64, i64))> = Vec::new();
    let mut groups: Vec<Vec<usize>> = Vec::from_iter((0..all.len()).map(|i| vec![i]));

    while groups.len() != 1 {
        for i in 0..all.len(){
            let res = match_pos(i, &mut all, &groups);
            if res.is_some(){
                let (c0, c1, rotation, translation) = res.unwrap();
                map_matches.push((c0, c1, rotation, translation));

                let (g0, _) = groups.iter().enumerate().find(|(_, g)| g.contains(&c0)).unwrap();
                let (g1, _) = groups.iter().enumerate().find(|(_, g)| g.contains(&c1)).unwrap();
                if g0 == g1{
                    panic!("ERROR, CANNOT HAVE BOTH IN SAME GROUP");
                }
                let mut g1_vals = groups[g1].clone();
                groups[g0].append(&mut g1_vals);
                groups.remove(g1);
            }
        }
    }

    let first  = stitch_cloud(&map_matches, &all).len();

    let zeros: Vec<Vec<(i64, i64, i64)>> = vec![vec![(0, 0, 0); 1]; all.len()];
    let tz = stitch_cloud(&map_matches, &zeros);
    let mut second = 0;
    for i0 in 0..all.len(){
        for i1 in 0..all.len(){
            let dist = (tz[i0].0 - tz[i1].0).abs() + (tz[i0].1 - tz[i1].1).abs() + (tz[i0].2 - tz[i1].2).abs();
            second = max(second, dist);
        }
    }
    println!("First:  {}", first);
    println!("Second: {}", second);
}
