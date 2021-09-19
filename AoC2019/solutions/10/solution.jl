#Advent of Code 2019 day 10
using DataStructures

input_path = (@__DIR__) * "/input"

function load(file_path=input_path)
    # Read data from file
    data = read((@__DIR__) * "/input", String)
    data = split(data, '\n')
    global height = length(data)
    global width = length(data[1])
    asteroids = []
    x , y = 0, 0

    for line in data
        for character in line
            if character == '#'
                push!(asteroids, (x, y))
            end
            x += 1
        end
        x = 0
        y += 1
    end
    return asteroids
end

#Calculating the angle in their way
function angle(point1, point2)
    #dx, dy = point2[1] - point1[1], point2[2] - point1[2]
    #return mod(atan(dy, dx) + pi/2, 2pi)
    #Get the atan2 angle, shift it by 90
    return mod(atan(point2[2] - point1[2], point2[1] - point1[1]) + pi/2, 2pi)
end

function task1(asteroids)
    #Result variables
    top = 0
    result = Nothing
    #Test for every asteroid
    for asteroid in asteroids
        #For unique elements
        counter = Set()
        for other in asteroids
            if other != asteroid
                #Add the angle to the set
                push!(counter, angle(asteroid, other))
            end
        end
        if length(counter) > top
            top = length(counter)
            result = asteroid
        end
    end
    flush(stdout)
    return top, result
end

function task2(asteroids)
    pos = 200
    asteroid_dict = DataStructures.SortedDict{Float64, Array{Any, 1}}()
    base = task1(asteroids)[2]

    #Fill dictionary
    for other in asteroids
        if other != base
            a = angle(base, other)
            if !haskey(asteroid_dict, a); asteroid_dict[a] = []; end
            push!(asteroid_dict[a], other)
        end
    end

    #Sort the lines of sight by distance to the base
    foreach(asteroid_line -> sort!(asteroid_line.second, by= x-> (x[1] - base[1])^2 + (x[2] - base[2])^2), asteroid_dict)

    index = 1
    while true
        for asteroid_line in asteroid_dict
            #If there is no more asteroids at that angle, ignore
            if length(asteroid_line) == 0
                continue
            end

            #Fetch asteroid
            asteroid = asteroid_line.second[1]
            if index == pos
                flush(stdout)
                return asteroid[1] * 100 + asteroid[2]
            end

            #Increment and delete asteroid
            index += 1
            deleteat!(asteroid_line.second, 1)
        end
    end
end


function solution()
    data = load()
    #println(data)
    println("First: $(task1(data)[1])")
    # Atom aint printin so we do it twice
    println("Second: $(task2(data))")
end

solution()
