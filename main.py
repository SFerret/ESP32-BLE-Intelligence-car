from machine import Pin, PWM
import bluetooth
import BLEsetup
import time

# 建立BLE对象（白鲸记裴廊德号）
Pequod = bluetooth.BLE()
# 导入BLE类（船长亚哈）
Ahab = BLEsetup.BLESimplePeripheral(Pequod)
ad = Pequod.config('mac')
print('mac地址为')
print(ad)

# 控制正转反转
IN1 = 2
IN2 = 4
IN3 = 16
IN4 = 17

# 五路循迹红外循迹引脚输入初始化
sw1 = Pin(25, Pin.IN)
sw2 = Pin(33, Pin.IN)
sw3 = Pin(32, Pin.IN)
sw4 = Pin(35, Pin.IN)
sw5 = Pin(34, Pin.IN)

# PWM调速
mo_l1 = PWM(Pin(IN1, Pin.OUT))
mo_l2 = PWM(Pin(IN2, Pin.OUT))
mo_r1 = PWM(Pin(IN3, Pin.OUT))
mo_r2 = PWM(Pin(IN4, Pin.OUT))

be = 0


def red_break(co):
    global be
    if co == b'stop\x00':
        be = 1
    else:
        be = 0


def motor_setup():
    mo_l1.duty_u16(0)
    mo_l1.freq(20000)
    mo_l2.duty_u16(0)
    mo_l2.freq(20000)
    mo_r1.duty_u16(0)
    mo_r1.freq(20000)
    mo_r2.duty_u16(0)
    mo_r2.freq(20000)


# 左转
def turn_left():
    mo_l1.duty_u16(40000)
    mo_l2.duty_u16(0)
    mo_r1.duty_u16(45000)
    mo_r2.duty_u16(0)
    Ahab.send('left')
    print('left')


# 右转
def turn_right():
    mo_l1.duty_u16(45000)
    mo_l2.duty_u16(0)
    mo_r1.duty_u16(40000)
    mo_r2.duty_u16(0)
    Ahab.send('right')
    print('right')


def fast_left():
    mo_l1.duty_u16(0)
    mo_l2.duty_u16(40000)
    mo_r1.duty_u16(48000)
    mo_r2.duty_u16(0)
    Ahab.send('fast_left')


def fast_right():
    mo_l1.duty_u16(48000)
    mo_l2.duty_u16(0)
    mo_r1.duty_u16(0)
    mo_r2.duty_u16(40000)
    Ahab.send('fast_right')


# 前进
def forward():
    mo_l1.duty_u16(40000)
    mo_l2.duty_u16(0)
    mo_r1.duty_u16(40000)
    mo_r2.duty_u16(0)
    Ahab.send('forward')
    print('forward')


def slow_forward():
    mo_l1.duty_u16(45000)
    mo_l2.duty_u16(0)
    mo_r1.duty_u16(45000)
    mo_r2.duty_u16(0)
    print('SF')
    Ahab.send('SF')


# 快速前进
def fast_forward():
    mo_l1.duty_u16(55000)
    mo_l2.duty_u16(0)
    mo_r1.duty_u16(55000)
    mo_r2.duty_u16(0)
    Ahab.send('fast_forward')
    print('fast_forward')


# 后退
def backward():
    mo_l1.duty_u16(0)
    mo_l2.duty_u16(40000)
    mo_r1.duty_u16(0)
    mo_r2.duty_u16(40000)
    Ahab.send('backward')
    print('backward')


# 停止
def stop():
    mo_l1.duty_u16(0)
    mo_l2.duty_u16(0)
    mo_r1.duty_u16(0)
    mo_r2.duty_u16(0)
    Ahab.send('stop')
    print('stop')


def loop_left():
    mo_l1.duty_u16(0)
    mo_l2.duty_u16(42000)
    mo_r1.duty_u16(42000)
    mo_r2.duty_u16(0)
    Ahab.send('loop_left')
    print('loop_left')


def loop_right():
    mo_l1.duty_u16(42000)
    mo_l2.duty_u16(0)
    mo_r1.duty_u16(0)
    mo_r2.duty_u16(42000)
    Ahab.send('loop_right')
    print('loop_right')


def error_left():
    mo_l1.duty_u16()
    mo_l2.duty_u16(32000)
    mo_r1.duty_u16(46000)
    mo_r2.duty_u16(0)


def error_right():
    mo_l1.duty_u16(46000)
    mo_l2.duty_u16(0)
    mo_r1.duty_u16(0)
    mo_r2.duty_u16(32000)


def loop_m_l():
    mo_l1.duty_u16(0)
    mo_l2.duty_u16(30000)
    mo_r1.duty_u16(30000)
    mo_r2.duty_u16(0)


def loop_m_r():
    mo_l1.duty_u16(30000)
    mo_l2.duty_u16(0)
    mo_r1.duty_u16(0)
    mo_r2.duty_u16(30000)


# 红外循迹程序
def red():
    global be
    Ahab.send('red')
    print('red')
    be = 0
    error = 0
    while True:
        Ahab.write(red_break)
        if be == 1:
            break
        else:
            if sw1.value() == 1 and sw2.value() == 1 and sw3.value() == 0 and sw4.value() == 1 and sw5.value() == 1:
                slow_forward()
                error = 0  # 识别黑线在中间，前进
                time.sleep(0.07)
            elif sw1.value() == 0 and sw2.value() == 0 and sw3.value() == 0 and sw4.value() == 0 and sw5.value() == 0:
                slow_forward()
                error = 0  # 识别路口前进
                time.sleep(0.07)
            elif sw1.value() == 1 and sw2.value() == 0 and sw3.value() == 0 and sw4.value() == 0 and sw5.value() == 1:
                slow_forward()
                error = 0  # 识别路口前进
                time.sleep(0.07)
            elif sw1.value() == 1 and sw2.value() == 0 and sw3.value() == 1 and sw4.value() == 1 and sw5.value() == 1:
                turn_left()
                error = -1  # 识别黑线偏左，左转
                time.sleep(0.07)
            elif sw1.value() == 0 and sw2.value() == 1 and sw3.value() == 1 and sw4.value() == 1 and sw5.value() == 1:
                fast_left()  # 识别黑线偏左，左转
                time.sleep(0.07)
                error = -1
            elif sw1.value() == 0 and sw2.value() == 0 and sw3.value() == 1 and sw4.value() == 1 and sw5.value() == 1:
                turn_left()
                error = -1  # 识别黑线偏左，左转
                time.sleep(0.07)
            elif sw1.value() == 0 and sw2.value() == 0 and sw3.value() == 0 and sw4.value() == 1 and sw5.value() == 1:
                fast_left()
                error = -1  # 识别黑线偏左，左转
                time.sleep(0.07)
            elif sw1.value() == 1 and sw2.value() == 0 and sw3.value() == 0 and sw4.value() == 1 and sw5.value() == 1:
                turn_left()
                error = -1
                time.sleep(0.07)
            elif sw1.value() == 1 and sw2.value() == 1 and sw3.value() == 1 and sw4.value() == 0 and sw5.value() == 1:
                turn_right()
                error = 1  # 识别黑线偏右，右转
                time.sleep(0.07)
            elif sw1.value() == 1 and sw2.value() == 1 and sw3.value() == 1 and sw4.value() == 1 and sw5.value() == 0:
                fast_right()
                error = 1  # 识别黑线偏右，右转
                time.sleep(0.07)
            elif sw1.value() == 1 and sw2.value() == 1 and sw3.value() == 1 and sw4.value() == 0 and sw5.value() == 0:
                turn_right()
                error = 1
                time.sleep(0.07)
            elif sw1.value() == 1 and sw2.value() == 1 and sw3.value() == 0 and sw4.value() == 0 and sw5.value() == 0:
                fast_right()
                error = 1  # 识别黑线偏右，右转,急转
                time.sleep(0.07)
            elif sw1.value() == 1 and sw2.value() == 1 and sw3.value() == 0 and sw4.value() == 0 and sw5.value() == 1:
                turn_right()
                error = 1
                time.sleep(0.07)  # 识别到右锐角
            elif sw1.value() == 0 and sw2.value() == 0 and sw3.value() == 0 and sw4.value() == 0 and sw5.value() == 1:
                fast_left()
                error = -1
                time.sleep(0.07)
            elif sw1.value() == 1 and sw2.value() == 0 and sw3.value() == 0 and sw4.value() == 0 and sw5.value() == 0:
                fast_right()
                error = -1
                time.sleep(0.07)
            elif sw1.value() == 1 and sw2.value() == 1 and sw3.value() == 1 and sw4.value() == 1 and sw5.value() == 1:
                if error == -1:
                    error_left()
                    time.sleep(0.07)
                elif error == 1:
                    error_right()
                    time.sleep(0.07)
                else:
                    backward()
                    time.sleep(0.1)
                    loop_left()
                    time.sleep(0.5)
                    loop_right()
                    time.sleep(0.5)
            else:
                slow_forward()
                error = 0
                time.sleep(0.05)
    stop()


# 蓝牙接受程序;.
def bluetooth_receive_setup(a):
    if a == b'forward\x00':
        fast_forward()
    elif a == b'backward\x00':
        backward()
    elif a == b'left\x00':
        loop_left()
    elif a == b'right\x00':
        loop_right()
    elif a == b'TL\x00':
        turn_left()
    elif a == b'TR\x00':
        turn_right()
    elif a == b'red\x00':
        red()
    elif a == b'stop\x00':
        stop()
    else:
        stop()


# 主程序
motor_setup()
stop()
Ahab.write(bluetooth_receive_setup)
