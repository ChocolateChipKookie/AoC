#Advent of Code 2020 day 5
input_path = (@__DIR__) * "/input"

function load(file_path=input_path)
    # Read data from file
    data = read((@__DIR__) * "/input", String)
    # Split into lines
    lines = split(strip(data), "\n")
    return lines
end

function calc_data(data)
    # Transforms the string of FBLR to binary number
    transform = Dict('F'=>'0', 'B'=>'1', 'L'=>'0', 'R'=>'1')
    data = [map(x -> transform[x], pid) for pid in data]
    # Parses binary to int and sorts the array
    return sort(parse.(Int, data; base=2))
end

function task1(data)
    # Max value of the data
    return data[end]
end

function task2(data)
    # Only value from [min, max] that is not present in the data
    return filter(x -> !(x in data), data[1]:data[end])[1]
end

function solution()
    data = load()
    #println(data)
    data = calc_data(data)
    println("First:  $(task1(data))")
    println("Second: $(task2(data))")
end

solution()

