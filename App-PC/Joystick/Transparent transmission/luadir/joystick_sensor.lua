set_global_variable("B5",1)

user = {0,0,0,0,0,0}
-- user = get_user_frame(0)
user_inv = pose_inv(user)
-- 获取用户坐标并求逆

p1j1,p1j2,p1j3,p1j4,p1j5,p1j6 = get_global_variable("P10")
p2j1,p2j2,p2j3,p2j4,p2j5,p2j6 = get_global_variable("P2")
p1_pose = get_fwd_kinematics({p1j1,p1j2,p1j3,p1j4,p1j5,p1j6,0,0})
p2_pose = get_fwd_kinematics({p2j1,p2j2,p2j3,p2j4,p2j5,p2j6,0,0})
trsf1 = pose_mul(user_inv,p1_pose)
trsf2 = pose_mul(user_inv,p2_pose)
-- 获取workspace对角线两给点在用户坐标系下的坐标

i = 0
j = 0
if trsf1[1]>trsf2[1]
then
    xmax = trsf1[1]
    xmin = trsf2[1]
end
if trsf1[1]<trsf2[1]
then
    xmax = trsf2[1]
    xmin = trsf1[1]
end
if trsf1[2]>trsf2[2]
then
    ymax = trsf1[2]
    ymin = trsf2[2]
end
if trsf1[2]<trsf2[2]
then
    ymax = trsf2[2]
    ymin = trsf1[2]
end
-- 设定手臂在workspace运动的最大范围

repeat
    repeat
        b5 = get_global_variable("B5")
        x = get_robot_io_status("a1")
        y = get_robot_io_status("a0")
        x = (x-4.5)/2
        y = -(y-4.5)/2
        -- 读取摇杆IO模拟输入
        if x<0.3 and x >-0.3
        then
            x = 0
        end
        if y<0.3 and y >-0.3
        then
            y = 0
        end
        -- 设定最小阈值
    
        if (x == 0) or (y == 0)
        then
            set_global_variable("B7",0)
        end
    
        if (x ~= 0) or (y ~= 0)
        then
            set_global_variable("B7",1)
        end
	sleep(0.001)
    until b5 == 0

    din4 = get_robot_io_status("i4")
    if din4 == 1 then
        set_global_variable("B5",1)
    end
    -- 监视按钮是否被触发

    x = get_robot_io_status("a1")
    y = get_robot_io_status("a0")
    x = -(x-4.5)/2
    y = -(y-4.5)/2
    -- 读取摇杆IO模拟输入

    fwd_p12 = get_robot_pose()
    -- 获取机器人当前空间坐标系位姿

    j1,j2,j3,j4,j5,j6 = get_global_variable("P12")
    fwd_p13 = {fwd_p12[1],fwd_p12[2],p2_pose[3],fwd_p12[4],fwd_p12[5],fwd_p12[6]}
    joint13 = get_inv_kinematics(fwd_p13,{j1,j2,j3,j4,j5,j6})
    set_global_variable("P13",joint13[1],joint13[2],joint13[3],joint13[4],joint13[5],joint13[6])

    trsf12 = pose_mul(user_inv,fwd_p12)
    -- 获取机器人当前用户坐标系位姿
    
    if x<0.3 and x >-0.3
    then
        x = 0
    end
    if y<0.3 and y >-0.3
    then
        y = 0
    end
    -- 设定最小阈值

    if trsf12[1]<xmin
    then
        if x<0
        then
            x = 0
        end
    end
    if trsf12[1]>xmax
    then
        if x>0
        then
            x = 0
        end
    end
    if trsf12[2]<ymin
    then
        if y<0
        then
            y = 0
        end
    end
    if trsf12[2]>ymax
    then
        if y>0
        then
            y = 0
        end
    end
    -- 运动范围控制

    if (x < 0 and i >= x) or ( x >= 0 and x < i ) then
        i = i - 0.05
    end
    if (x > 0 and i <= x) or ( x <= 0 and x > i ) then
        i = i + 0.05
    end
    if (x < 0 and i <= x) or ( x > 0 and i >= x ) then
        i = x
    end
    if (y < 0 and j >= y) or ( y >= 0 and y < j ) then
        j = j - 0.05
    end
    if (y > 0 and j <= y) or ( y <= 0 and y > j ) then
        j = j + 0.05
    end
    if (y < 0 and j <= y) or (y > 0 and j >= y) then
        j = y
    end
    -- 运动加速度控制


    trsf12[1] = trsf12[1] + i
    trsf12[2] = trsf12[2] + j
    fwd_p12 = pose_mul(user,trsf12)
    -- 将用户坐标系下位移转为空间坐标系位移

    j1,j2,j3,j4,j5,j6 = get_global_variable("P12")
    joint12 = get_inv_kinematics(fwd_p12,{j1,j2,j3,j4,j5,j6})
    set_global_variable("P12",joint12[1],joint12[2],joint12[3],joint12[4],joint12[5],joint12[6])
    sleep(0.008)

until(false)
