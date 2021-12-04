#Advent of Code 2021 day 3
input_path = (@__DIR__) * "/input"

function load(file_path=input_path)
    # Read data from file
    data = read((@__DIR__) * "/input", String)
    # Split into lines
    lines = split(strip(data), "\n")
    return lines
end

function task1(data)
    return Nothing
end
    
function task2(data)
    return Nothing
end


function solution()
    data = load()
    #println(data)
    println("First: $(task1(data))")
    println("Second: $(task2(data))")
end
    
solution()
