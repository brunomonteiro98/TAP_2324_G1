-- communication with backyard gripper 
-- version 1.0 
-- 功能实现 1， 校准，
--         2， 可以通过D1-D4 设置位置，速度，加速度，加持力的移动指令。
--         3， 状态获取（待验证）
-- 功能待实现 1， 获取是否calibration 的状态
--           2， 如何判断执行完毕而进行下一部动作，而不是靠延迟一个时间。





--字符串分割
function string.split(str,delimiter)
	if str == nil or str == '' or delimiter == nil then
		return nil
	end
	local result = {}
	for match in (str..delimiter):gmatch("(.-)"..delimiter) do
		table.insert(result,tonumber(match))
	end
	return result
end

function moveTO(IP, pose, speed, acc, torque, tolerance, waitFlag)
	local tolerance = tolerance or 90
	local waitFlag = waitFlag or "True"
	local cmd = "moveTo"
	local cmd_args = cmd  .. string.format("(%s,%s,%s,%s,%s,%s)", pose, speed, acc, torque, tolerance, waitFlag)  .. "\n"
	-- print('cmd_args_moveTo',cmd_args)
	local a = client_send_data(IP,cmd_args)
	return a
end

--校准夹爪
function calibrateGripper(IP)
	local cmd_args = "calibrateGripper()" .. "\n" 
	local a = client_send_data(IP,cmd_args)
	return a
end
--获取夹爪状态
function getStatus(IP)
    local cmd_args = "getStatus()" .. "\n"
    local a = client_send_data(IP,cmd_args)
	local b,c=client_recv_data (IP,1)
	return c
end

function getCalibrated(IP)
	local cmd_args = "getCalibrated()" .. "\n"
	local a = client_send_data(IP,cmd_args)
	return a 
end

-- 状态结果处理
function process_getresult(str)
	local str_tmp = {}
	str_tmp = string.gsub(str,"%[",'')
	str_tmp = string.gsub(str_tmp,"%]",'')
	local res = string.split(str_tmp,',')
	return res
end
--夹爪重启
function restart(IP)
	local cmd_args = "restart()" .. "\n"	
	local a = client_send_data(IP,cmd_args)
	return a
end
--夹爪关闭
function shutdown(IP)
	local cmd_args = "shutdown()" .. "\n"
	local a = client_send_data(IP,cmd_args)
	return a
end



-- initialization
set_global_variable("D11",0)  -- 设置位置默认值为0
set_global_variable("D12",999) -- 设置速度默认值为999
set_global_variable("D13",700) -- 设置加速度默认值为700
set_global_variable("D14",0.5) -- 设置加持力为百分之50
-- connection 
IP = "192.168.1.9"  -- 夹爪IP
PORT = 9999 -- 夹爪端口号
repeat
    elite_print("Gripper connecting")
    connect = connect_tcp_server(IP,PORT)
    sleep(1)
until connect == 1
elite_print("Gripper connected")
set_global_variable("D10",1)
while true do 
	sleep(0.01)
	a = get_global_variable("D10")
	-- elite_print(a)
	if a == 1 then 
	-- calibration 校准
		--elite_print('Gripper calibrating-------')
		local res = calibrateGripper(IP)
		set_global_variable("D10",0)
	elseif a == 2 then 
		-- 移动任务 
		--elite_print("Gripper moving")
		local pos = get_global_variable("D11")
		local speed = get_global_variable("D12")
		local acc = get_global_variable("D13")
		local force = get_global_variable("D14")
		local res = moveTO(IP,pos,speed,acc,force)
		set_global_variable("D10",0)
	elseif a ==3 then 
		--elite_print('Gripper open')
		print(moveTO(IP, 100,  999, 700, 0.5))
		set_global_variable("D10",0)
	elseif a == 4 then
        -- 获取calibration 状态
		--elite_print("Gripper status") 
		local status = getStatus(IP)
		local tmp = process_getresult(status)
		for i,v in ipairs(tmp) do 
			set_global_variable(string.format("D%d",19+i),v)
		end
		set_global_variable("D10",0)
	
	elseif a == 5 then 
		--elite_print("Gripper restarting gripper")
		restart(IP)
		set_global_variable("D10",0)
	elseif a == 6 then 
		--elite_print("Gripper shut down")
		shutdown(IP)
		set_global_variable("D10",0)
	end
end






