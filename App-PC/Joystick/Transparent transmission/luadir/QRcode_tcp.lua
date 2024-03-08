scanner = "192.168.1.111"
repeat
    connect = connect_tcp_server(scanner,2000)
    elite_print("waiting for scanner")
    sleep(1)
until( connect == 1)
    
sleep(1)
elite_print("connected")
set_global_variable("B20",0)

repeat

    repeat
        ret,recv_buff = client_recv_data(scanner,1,1)
        endword = string.sub(recv_buff,9,12) 
    until(ret == 6 and endword == "0D0A")

    pswd_ascii = string.char("0x"..string.sub(recv_buff,1,2))..string.char("0x"..string.sub(recv_buff,3,4))..string.char("0x"..string.sub(recv_buff,5,6))..string.char("0x"..string.sub(recv_buff,7,8))
    pswd_ascii = tonumber(pswd_ascii)
    elite_print(pswd_ascii)
    
    -- 使用0000的QRcode清空已使用密码文件
    if (pswd_ascii == 0) then
        file = io.open("used.txt", "w")
        io.output(file)
        io.close(file)
    
    -- 万用密码
    elseif (pswd_ascii == 3548) then
        y1=get_robot_io_status("o1")
        y2=get_robot_io_status("o2")
        if y1==1 and y2==0 then
            set_global_variable("B20",1)
            sleep(1)
            set_global_variable("B20",0)
        end
    else
        -- 检查是否重叠已使用过的密码
        for check in io.lines("used.txt") do
            if (pswd_ascii == tonumber(check)) then
                used = true
            end
        end
        -- 若未使用过则输出变量，且将新密码加入已使用的密码文件
        if used == false then
            for line in io.lines("pswd.txt") do
                if (pswd_ascii==tonumber(line)) then
                    elite_print("match!")
                    file = io.open("used.txt","a")
                    io.output(file)
                    io.write(pswd_ascii.."\n")
                    io.close(file)
                    y1=get_robot_io_status("o1")
                    y2=get_robot_io_status("o2")
                    if y1==1 and y2==0 then
                        set_global_variable("B20",1)
                        sleep(1)
                        set_global_variable("B20",0)
                    end
                end
            end
        end
        used = false
    end

until(false)
