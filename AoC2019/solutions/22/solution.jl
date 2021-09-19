#Advent of Code 2019 day 22
input_path = (@__DIR__) * "/input"

function task1()
    #Loading maze
    file = split(read(input_path, String), "\n")
    file = filter!(x-> length(x) > 0, file)

    #Creating deck
    deck_size = 10007
    deck = [0:1:(deck_size - 1);]

    #Shuffling
    for line in file
        tokens = split(line)
        #Cutting
        if tokens[1] == "cut"
            position = mod1(parse(Int64, tokens[2]) + 1, length(deck))
            new_deck = Array{Int64, 1}(undef, length(deck))
            for i in 1:length(deck)
                new_deck[i] = deck[position]
                position = mod1(position + 1, length(deck))
            end
            deck = new_deck
        #Deal
        elseif tokens[2] == "into"
            reverse!(deck)
        #Deal with increment
        else
            increment = parse(Int64, tokens[4])
            deck_size = length(deck)
            new_deck = fill(-1, deck_size)
            index = 1
            for i in 1:deck_size
                new_deck[index] = deck[i]
                index = mod1(index + increment, deck_size)
            end
            deck = new_deck
        end
    end

    flush(stdout)
    return findall(x->x == 2019, deck)[1] - 1
end

#This is a lot of math that I did not come up with. I now understand it but I totally needed help.
function task2()
    file = split(read(input_path, String), "\n")
    file = filter!(x-> length(x) > 0, file)

    #Variables
    deck_size::BigInt = 119315717514047
    repeats::BigInt = 101741582076661
    card_pos::BigInt = 2020

    #Increment and offset
    increment::BigInt = 1
    offset::BigInt = 0

    #Creating the modulo math thingie
    for line in file
        tokens = split(line)
        #Cutting
        if tokens[1] == "cut"
            offset += increment * parse(Int128, tokens[2])
        #Deal
        elseif tokens[2] == "into"
            increment = -increment
            offset += increment
        #Deal with increment
        else
            increment *= invmod(parse(Int128, tokens[4]), deck_size)
        end
    end

    #Lots of modulo math
    total_increment::BigInt = powermod(increment, repeats, deck_size)
    total_offset::BigInt = offset * (1 - total_increment) * invmod(1 - increment, deck_size)

    #Result
    result::BigInt = mod(total_offset + total_increment * card_pos, deck_size)
    flush(stdout)
    return result
end


function solution()
    #println(data)
    println("First: $(task1())")
    println("Second: $(task2())")
end

solution()
