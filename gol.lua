

c=5
r=5
w=5
neigh=0

land = {} 
for i=1,c do
    land[i] = {}
    for j=1,r do
    land[i][j] = 0
    end
end

function print_land()        
        for i = 1, c+2 do
            io.write('*')
        end
        print('')
        for i = 1, c do
            io.write('*')
            for j = 1, r do
                if land[i][j] == 0 then
                    io.write('.')
                else 
                    io.write('O')
                end
            end
            print('*')
        end 
        for i = 1, c+2 do
            io.write('*')
        end
        print('')
end


-- for i=2,(c-1) do
--     for j=2,(r-1) do
--         if(math.random(100)<50) then
--             land[i][j] = 1
--         else
--             land[i][j] = 0
--         end

--     end
-- end
--next step

--land[2][2], land[2][3], land[2][4] = 1, 1, 1
land[2][2], land[3][2], land[4][2] = 1, 1, 1

print_land()


function next_gen()

    next = {} 
    for i=1,c do
        next[i] = {}
        for j=1,r do
            next[i][j] = 0
        end
    end


    for i = 1, c do
            for j = 1, r do
                local s = 0
                for p = i-1,i+1 do
                    for q = j-1,j+1 do
                        if p > 0 and p <= c and q > 0 and q <= r then
                            s = s + land[p][q]
                        end
                    end
                end
                s = s - land[i][j]
                if s == 3 or (s+land[i][j]) == 3 then
                    next[i][j] = 1
                else
                    next[i][j] = 0
                end
            end
        end

    return next

end    


land = next_gen()
print_land()
land = next_gen()
print_land()
land = next_gen()
print_land()
land = next_gen()
print_land()
land = next_gen()
print_land()
land = next_gen()
print_land()
print_land()
