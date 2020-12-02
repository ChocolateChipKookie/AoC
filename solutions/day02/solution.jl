# Define input path
input_path = (@__DIR__) * "/input"

function load(file_path=input_path)
    # Read data from file
    data = read((@__DIR__) * "/input", String)
    # Split into lines
    lines = split(strip(data), "\n")
    # Create named tuple from data
    return [
            (
            range    = parse.(Int, split(x[1], '-')),
            value    = x[2][1],
            password = x[3]
            )   for x in [split(x) for x in lines]]
end

function task1(data)
    """
    Return number of passwords that meet the condition:
        first <= occurances(value, password) <= second
    """
    return count(
        p -> p.range[1] <= count(x-> x == p.value, p.password) <= p.range[2],
        data)
end

function task2(data)
    """
    Return number of passwords that meet the condition:
        (password[first] == value) xor (password[second] == value)
    """
    return count(
        p -> (p.password[p.range[1]] == p.value) != (p.password[p.range[2]] == p.value),
        data)
end

function solution()
    data = load()
    println("First: $(task1(data))")
    println("Second: $(task2(data))")
end

@time solution()
