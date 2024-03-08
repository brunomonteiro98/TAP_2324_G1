-- 力感测
function hex2float( hexString )
	if hexString == nil then
		return 0
	end
	local t = type( hexString )
	if t == "string" then
		hexString = tonumber(hexString , 16)
	end
 
	local hexNums = hexString
 
	local sign = math.modf(hexNums/(2^31))
 
	local exponent = hexNums % (2^31)
	exponent = math.modf(exponent/(2^23)) -127
 
	local mantissa = hexNums % (2^23)
 
	for i=1,23 do
		mantissa = mantissa / 2
	end
	mantissa = 1+mantissa
	local result = (-1)^sign * mantissa * 2^exponent
	return result
end

function str2hex(str)
	--判断输入类型	
	if (type(str)~="string") then
	    return nil,"str2hex invalid input type"
	end
	--滤掉分隔符
	str=str:gsub("[%s%p]",""):upper()
	--检查内容是否合法
	if(str:find("[^0-9A-Fa-f]")~=nil) then
	    return nil,"str2hex invalid input content"
	end
	--检查字符串长度
	if(str:len()%2~=0) then
	    return nil,"str2hex invalid input lenth"
	end
	--拼接字符串
	local index=1
	local ret=""
	for index=1,str:len(),2 do
	    ret=ret..string.char(tonumber(str:sub(index,index+1),16))
	end
 
	return ret
end

function hex2str(hex)
	--判断输入类型
	if (type(hex)~="string") then
		return nil,"hex2str invalid input type"
	end
	--拼接字符串
	local index=1
	local ret=""
	for index=1,hex:len() do
		ret=ret..string.format("%02X",hex:sub(index):byte())
	end
 
	return ret
end

function convert(hex )
	-- body
	hex = string.reverse(hex)
	local hex_str = hex2str(hex)
	return hex2float(hex_str)
end
-- rs485 parameter
spd = 460800
bits = 8
event = "N"
stop = 1
set_global_variable("B4",0)
sleep(1)
local open = rs485_open()

if open >= 0 then 
    
    local set = rs485_setopt(spd,bits,event,stop)
    sleep(1)
    
	rs485_send("47AA0D0A",1)
	sleep(1)
	elite_print("sensor initialized, waiting...")

	rs485_send("49AA0D0A",1)
	elite_print("first_refresh")
	sleep(1)
	elite_print("refreshing")
	
	repeat
	
		repeat
			local lenth = rs485_send("49AA0D0A",1)
			ret,recv_buff = rs485_recv(100,1)
			begin = string.sub(recv_buff,0,4)
		until(ret ==28 and begin == "49AA")
		local hex = str2hex(recv_buff)
		local f1 = string.sub(hex,3,7)
		local f2 = string.sub(hex,7,11)
		local f3 = string.sub(hex,11,15)
		local f4 = string.sub(hex,15,19)
		local f5 = string.sub(hex,19,23)
		local f6 = string.sub(hex,23,27)
		F1 = convert(f1)
		F2 = convert(f2)
		F3 = convert(f3)
		F4 = convert(f4)
		F5 = convert(f5)
		F6 = convert(f6)
		set_global_variable("D1",F1)
		set_global_variable("D2",F2)
		set_global_variable("D3",F3)
		set_global_variable("D4",F4)
		set_global_variable("D5",F5)
		set_global_variable("D6",F6)
	
	until(false)

else 
    elite_print("open dead")
end

rs485_close()