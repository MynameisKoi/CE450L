def PID():
    Kp = 8
    Ki = 5
    Kd = 1.6
    error = [30,20,10,7,5,2,1,-3,3]
    ctrl_signal_u = 394
    for i in range(2,len(error)):
        delta_u = Kp*(error[i] - error[i-1]) + Ki*error[i] + Kd*(error[i]-2*error[i-1]+error[i-2])
        # format delta_u 2 decimal points
        print('delta_u_', i, '=', "{:.2f}".format(delta_u))
        ctrl_signal_u += delta_u
        print('u_', i, '=', "{:.2f}".format(ctrl_signal_u))

PID()