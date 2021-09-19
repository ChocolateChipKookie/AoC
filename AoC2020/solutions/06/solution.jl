#Advent of Code 2020 day 6
input_path = (@__DIR__) * "/input"

function load(file_path=input_path)
    # Read data from file
    data = read((@__DIR__) * "/input", String)
    # Split into lines
    groups = split(strip(data), "\n\n")
    # Split groups into individuals
    return [split(group) for group in groups]
end

function task1(data)
    groups_unique = [Set(join(group)) for group in data]
    return sum(length(x) for x in groups_unique)
end

function task2(data)
    # Create a set for every member in group
    groups_members = [[Set(line) for line in group] for group in data]
    # Create intersection for every group, between all the members of the group
    intersection = [intersect(x...) for x in groups_members]
    return sum(length(x) for x in intersection)
end


function solution()
    data = load()
    println("First:  $(task1(data))")
    println("Second: $(task2(data))")
end

solution()
