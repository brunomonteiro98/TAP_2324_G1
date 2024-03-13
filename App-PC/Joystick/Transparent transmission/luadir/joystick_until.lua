repeat
    repeat
        b5 = get_global_variable("B5")
    until b5 == 1

    repeat
        button = get_robot_io_status("i4")
    until button == 0

    repeat
        button = get_robot_io_status("i4")
        force = get_global_variable("D3")
        if (button == 1 or force <= -1) then
            set_global_variable("B6",1)
        end
        b5 = get_global_variable("B5")
    until b5 == 0

until(false)