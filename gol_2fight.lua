

c=10
r=10
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
                    io.write(' ')
                end    
                if land[i][j] == 1 then
                    io.write('+')
                end    
                if land[i][j] == 2 then
                    io.write('o')    
                end
            end
            print('*')
        end 
        for i = 1, c+2 do
            io.write('*')
        end
        print('')
end

math.randomseed(tostring(os.time()):reverse():sub(1,6))
for i=1,c do
    for j=1,r do        
        local v = math.random(100)
        -- print('v:'..v)
        land[i][j] = v
        if(v<66) then
            land[i][j] = 0
        elseif v<90 then 
            land[i][j] = 1
        else 
            land[i][j] = 2    
        end

    end
end
--next step

--land[2][2], land[2][3], land[2][4] = 1, 1, 1
-- land[2][2], land[3][2], land[4][2], land[5][1] = 1, 2, 1, 2

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
                local b = 0
                local w = 0
                local life_i_j = 0
                if land[i][j] > 0 then
                    life_i_j = 1
                    -- if land[i][j] == 1 then
                    --     b = 1
                    -- end    
                    -- if land[i][j] == 2 then
                    --     w = 1    
                    -- end    
                end
                for p = i-1,i+1 do
                    for q = j-1,j+1 do
                        if p > 0 and p <= c and q > 0 and q <= r then
                            if land[p][q] > 0 then                              
                                s = s + 1
                            end    
                            if land[p][q] == 1 then
                                b = b + 1
                            end    
                            if land[p][q] == 2 then
                                w = w + 1                                 
                            end    
                        end
                    end
                end                
                s = s - life_i_j

                -- print('i:'..i..'j:'..j)
                -- print('s:'..s)
                -- print('b:'..b)
                -- print('w:'..w)
                if s == 3 or (s+life_i_j) == 3 then
                    if life_i_j == 0 then
                        if b > w then
                            next[i][j] = 1
                        end    
                        if w > b then
                            next[i][j] = 2  
                        end    
                    else 
                       next[i][j] = land[i][j]
                    end     
                else
                    next[i][j] = 0
                end
            end
    end

    return next

end    



for l=1,50 do
    land = next_gen()
    print_land()
end

