#Advent of Code 2020 day 3
input_path = (@__DIR__) * "/input"

function load(file_path=input_path)
    # Read data from file
    data = read((@__DIR__) * "/input", String)
    # Split into lines
    lines = split(strip(data), "\n")
    return hcat([collect(x) for x in lines]...)
end

function countTrees(data, slope)
    pos = [1, 1]
    width, height = size(data)
    result = 0
    while pos[2] <= height
        if data[pos...] == '#'
            result += 1
        end
        pos += slope
        pos[1] = mod1(pos[1], width)
    end
    return result
end

function countTreesGlof(d, s)
    return count(y -> (y*s[2] < size(d)[2] && d[mod1(y*s[1] + 1, size(d)[1]), y*s[2] + 1] == '#'), 0:size(d)[2])
end

function task1(data)
    return countTrees(data, [3, 1])
end

function task2(data)
    slopes = [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]
    return prod(countTrees(data, slope) for slope in slopes)
end


function solution()
    data = load()
    println("First:  $(task1(data))")
    println("Second: $(task2(data))")
end

"""
First:  278
Second: 9709761600
"""
solution()