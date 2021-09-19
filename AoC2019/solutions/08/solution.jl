#Advent of Code 2019 day 8
input_path = (@__DIR__) * "/input"

function load(file_path=input_path)
    # Read data from file
    data = read((@__DIR__) * "/input", String)
    width, height = 25, 6
    size = width * height
    layers = div(length(data) , size)
    return data, (width, height, size, layers)
end

function task1(data)
    result = 0
    width, height, size, layers = data[2]
    data = data[1]
    min_zeros = size

    for i in 0:layers-1
        c = count(x->x=='0', data[i*size + 1: i*size + size])
        if c < min_zeros
            min_zeros = c
            result = count(x->x=='1', data[i*size + 1: i*size + size]) * count(x->x=='2', data[i*size + 1: i*size + size])
        end
    end
    return result
end

function task2(data)
    width, height, size, layers = data[2]
    data = data[1]
    result = fill('x', (width, height))

    for i in length(data):-1:1
        if data[i] != '2'
            result[mod1(mod1(i, size), width), cld(mod1(i, size), width)] = data[i]
        end
    end

    function stringify()
        res = "\n"
        for y in 1:height
            for x in 1:width
                if result[x, y] == '0'
                    res *= ' '
                elseif result[x, y] == '1'
                    res *= '#'
                end
            end
            res *= '\n'
        end
        return res
    end

    return stringify()
end

function solution()
    data = load()
    #println(data)
    println("First: $(task1(data))")
    println("Second: $(task2(data))")
end

solution()
