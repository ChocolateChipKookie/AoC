#Advent of Code 2019 day 16
input_path = (@__DIR__) * "/input"

function load(file_path=input_path)
    data = read((@__DIR__) * "/input", String)
    input = map(x-> x - '0', collect(strip(data)))
    return input
end

function calculate_phase(input, result)
    for x in 1:length(input)
        len = x * 4
        result[x] = 0
        for j in 0:(x-1)
            start = x + j
            for i in start:len:length(input)
                result[x] += input[i]
            end

            for i in (start + div(len, 2)):len:length(input)
                result[x] -= input[i]
            end
        end
        result[x] = string(result[x])[end] - '0'
    end
end

function calculate_phase_from_offset(input, offset)
    total = 0
    len = length(input)
    for x in len:-1:offset
        #As the second half is only a triangular matrix, it is only additions
        #When only adding we can get the last digit with the mod operation
        total += input[x]
        input[x] = mod(total, 10)
    end
end

function task1(input)
    result = Array{Int64, 1}(undef, length(input))
    #Number of iterations is divisible by 2, this way, the arrays are created only once
    for i in 1:div(100, 2)
        calculate_phase(input, result);
        calculate_phase(result, input)
    end
    #Printing
    flush(stdout)
    return prod(map(x->string(x), input[1:8]))
end

function task2(input)
    input = repeat(input, 10000)
    offset = parse(Int64, prod(map(x->string(x), input[1:7])))

    #We only need to calculate the second half of the matrix because the result is there and it is a triangular matrix
    #Only the stuff after the offset actually matters
    for i in 1:100
        calculate_phase_from_offset(input, offset)
    end
    flush(stdout)
    return prod(map(x->string(x), input[offset + 1:offset + 8]))
end


function solution()
    data = load()
    #println(data)
    # Atom sometimes does not print
    println("First: $(task1(data))")
    data = load()
    println("Second: $(task2(data))")
end

solution()
