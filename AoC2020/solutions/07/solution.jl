#Advent of Code 2020 day 7
input_path = (@__DIR__) * "/input"

function load(file_path=input_path)

    # Read data from file
    data = read((@__DIR__) * "/input", String)
    # Split into lines
    lines = split(strip(data), "\n")
    # Parse lines
    res = Dict()
    for line in lines
        bag, children = split(line, " bags contain ")
        if children == "no other bags."
            children = []
        else
            children = [split(child) for child in split(children, ", ")]
            children = [(join(tokens[2:3], " "), parse(Int, tokens[1])) for tokens in children]
        end
        res[bag] = children
    end
    return res
end

function task1(data)
    can_access = Set()

    function recursion(bag, goal)
        children = [c[1] for c in data[bag]]
        # If goal is in children or (any of the children(already evaluated as can_access or recursive==True))
        res = (goal in children) || any(c in can_access || recursion(c, goal) for c in children)
        if res
            push!(can_access, bag)
        end
        return res
    end

    for bag in data
        recursion(bag[1], "shiny gold")
    end

    flush(stdout)
    return length(can_access)
end


function task2(data)
    function recursion(bag)
        children = data[bag]
        # Sum of all children + 1 for this bag
        res = Array{Int, 1}([c[2] * recursion(c[1]) for c in children])
        return sum(res) + 1
    end

    return recursion("shiny gold") - 1
end


function solution()
    data = load()
    println("First:  $(task1(data))")
    println("Second: $(task2(data))")
end

solution()
