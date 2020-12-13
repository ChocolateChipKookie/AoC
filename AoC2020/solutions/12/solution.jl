#Advent of Code 2020 day 12
input_path = (@__DIR__) * "/input"

function load(file_path=input_path)
    # Read data from file
    data = read((@__DIR__) * "/input", String)
    # Split into lines
    lines = split(strip(data), "\n")
    return [ (x[1], parse(Int, x[2:end])) for x in lines]
end

function task1(data)
    current_pos = [0, 0]
    current_direction = 0
    commands = Dict()
    commands['N'] = x -> current_pos[2] += x
    commands['S'] = x -> current_pos[2] -= x
    commands['E'] = x -> current_pos[1] += x
    commands['W'] = x -> current_pos[1] -= x

    commands['L'] = x -> current_direction += x
    commands['R'] = x -> current_direction -= x
    commands['F'] =
    function(f)
        angle = current_direction*pi/180
        current_pos[2] += Int(round(sin(angle))) * f
        current_pos[1] += Int(round(cos(angle))) * f
    end

    for command in data
        commands[command[1]](command[2])
    end

    flush(stdout)
    return sum(map(abs, current_pos))
end

function task2(data)
    current_pos = [0, 0]
    current_waypoint = [10, 1]
    commands = Dict()
    commands['N'] = x -> current_waypoint[2] += x
    commands['S'] = x -> current_waypoint[2] -= x
    commands['E'] = x -> current_waypoint[1] += x
    commands['W'] = x -> current_waypoint[1] -= x

    function rotate(angle)
        if angle < 0
            angle += 360
        end
        for _ in 1:(angle/90)
            tmp = current_waypoint[1]
            current_waypoint[1] = -current_waypoint[2]
            current_waypoint[2] = tmp
        end
    end

    commands['L'] = x -> rotate(x)
    commands['R'] = x -> rotate(-x)
    commands['F'] =
    function(f)
        for _ in 1:f
            current_pos += current_waypoint
        end
    end

    for command in data
        commands[command[1]](command[2])
        println(command, current_pos, current_waypoint)
    end

    flush(stdout)
    return sum(map(abs, current_pos))
end


function solution()
    data = load()
    println(data)
    println("First: $(task1(data))")
    println("Second: $(task2(data))")
end

solution()
