# Define input path
input_path = (@__DIR__) * "/input"

function load(file_path=input_path)
    data = read((@__DIR__) * "/input", String)
    parse.(Int, split(data))
end

function task1(data)
    for i in data
        for j in data
            if i + j == 2020
                return i * j
            end
        end
    end
end

function task2(data)
    for i in data
        for j in data
            for k in data
                if i + j + k == 2020
                    return i * j * k
                end
            end
        end
    end
end

function solution()
    data = load()
    println("First:  $(task1(data))")
    println("Second: $(task2(data))")
end

"""
First:  158916
Second: 165795564
"""
solution()
