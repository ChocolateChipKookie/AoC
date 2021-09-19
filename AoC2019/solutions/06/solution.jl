#Advent of Code 2019 day 6
input_path = (@__DIR__) * "/input"

#Declare mutable struct Node
mutable struct Node
    children::Array{String}
    parent::String
    value::String
end

function load(file_path=input_path)
    # Read data from file
    data = read((@__DIR__) * "/input", String)
    tokens = split(data)

    dict = Dict()
    #Parse the tree
    for entry in tokens
        s = split(entry, ')')
        node = s[2]
        parent = s[1]

        if haskey(dict, node)
            dict[node].parent = parent
        else
            dict[node] = Node([], parent, node)
        end

        if !haskey(dict, parent)
            p = Node([], "", parent)
            dict[parent] = p
        end
        push!(dict[parent].children, node)
    end

    return dict
end

function task1(data)
    total = 0
    function recursive_fall(value, depth)
        total += depth
        for child in data[value].children
            recursive_fall(child, depth + 1)
        end
    end

    recursive_fall("COM", 0)
    return total
end

function task2(data)
    function depth(value)
        if value == "COM"
            return 0
        end
        return depth(data[value].parent) + 1
    end

    you = "YOU"
    santa = "SAN"
    you_d = depth(you)
    santa_d = depth(santa)
    total = 0
    if you_d < santa_d

        for i = 1:(santa_d-you_d)
            santa = data[santa].parent
            total += 1
        end
    elseif santa_d < you_d
        for i = 1:(you_d-santa_d)
            you = data[you].parent
            total += 1
        end
    end

    while data[santa].parent != data[you].parent
        you = data[you].parent
        santa = data[santa].parent
        total += 2
    end

    return total
end


function solution()
    data = load()
    #println(data)
    println("First: $(task1(data))")
    println("Second: $(task2(data))")
end

solution()
