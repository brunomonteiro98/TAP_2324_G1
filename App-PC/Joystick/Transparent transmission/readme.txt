backyard_gripper.lua————————————————————The Driver of Backyard Grippe（tcp）
	Position——D11
	Velocity——D12
	Accelerate——D13
	Force————D14
	Run——D0=2

joystick_sensor———————————Rocker Control（Analog Value）
	P10——Stop position And diagonal high position
	P2---diagonal high position
	P12--rocker control transparent transmission position
	p14--Feeding point


joystick_until————————————Rocker control
	IN4——-Start to grasp
	B6=1 -----complete grasp


ft_sensor—————————Force control sensor（485）
		D3------the force of Z direction


QRcode_tcp————————————————Scan QRcode Control（tcp）
	Scan QR Code finished B20=1
	
	
Y1______Green Light（Free to scan QRcode）

Y2______Red Light（Cannot scan QRcode）

joystick.jbi————————————————jbi 



Process。
1，Robot Power on , start all lua

2.move to P10，run jbi automatically


