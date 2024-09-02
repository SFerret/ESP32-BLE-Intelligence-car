# 基于ESP32的蓝牙循迹无线充电小车
序言：
* 程序基础
* 操控实现
* 红外循迹实现
* 蓝牙
* 无线充电

## 程序

使用MicroPython编程，利用Python丰富的库，快速完成程序的开发编写。

## 小车操控实现

利用在L298N的IN1~IN2通道分别输入PWM信号，来完成对电机速度、转动方向的控制。
```python
from machine import Pin, PWM
IN1 = 2
IN2 = 4
IN3 = 16
IN4 = 17

mo_l1 = PWM(Pin(IN1, Pin.OUT))
mo_l2 = PWM(Pin(IN2, Pin.OUT))
mo_r1 = PWM(Pin(IN3, Pin.OUT))
mo_r2 = PWM(Pin(IN4, Pin.OUT))


def slow_forward():
    mo_l1.duty_u16(40000)
    mo_l2.duty_u16(0)
    mo_r1.duty_u16(40000)
    mo_r2.duty_u16(0)

```
## 小车循迹实现

通过红外循迹模块输入单片机的数字信号,判断小车偏离黑线程度，由于时间和成本的限制，使用五路红外开关循迹模块，效果较查，可以使用八路灰度循迹，便于后续使用编写PID。
```python
from machine import Pin
sw1 = Pin(25, Pin.OUT)
sw2 = Pin(33, Pin.OUT)
sw3 = Pin(32, Pin.OUT)
sw4 = Pin(35, Pin.OUT)
sw5 = Pin(34, Pin.OUT)

if sw1.value() == 1 and sw2.value() == 1 and sw3.value() == 1 and sw4.value() == 1 and sw5.value() == 1:
    pass
if sw2.value() == 1 and sw2.value() == 0 and sw3.value() == 0 and sw4.value() == 1 and sw5.value() == 1:
    pass
```

## 小车蓝牙参考MicroPython官方在Github给出的示例文件，实现ESP32的BLE调用

>https://github.com/micropython/micropython/blob/master/examples/bluetooth/ble_simple_central.py

```python
import bluetooth
import struct
from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_FLAG_READ = const(0x0002)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)

_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)
_ADV_TYPE_UUID16_COMPLETE = const(0x3)
_ADV_TYPE_UUID32_COMPLETE = const(0x5)
_ADV_TYPE_UUID128_COMPLETE = const(0x7)
_ADV_TYPE_UUID16_MORE = const(0x2)
_ADV_TYPE_UUID32_MORE = const(0x4)
_ADV_TYPE_UUID128_MORE = const(0x6)
_ADV_TYPE_APPEARANCE = const(0x19)
                             
_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (
    bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_READ | _FLAG_NOTIFY,
)
_UART_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_WRITE | _FLAG_WRITE_NO_RESPONSE,
)
_UART_SERVICE = (
    _UART_UUID,
    (_UART_TX, _UART_RX),
)
```
通过手机的蓝牙串口软件向小车发送指令实现对小车方向控制，及小车循迹模式的开启

## 小车无线充电

发射端构建硬件，搭建逆变器，将DC输入转为AC正弦波输出，通过线圈发射实现无线充电；受电端通过先去接受AC交流电源，通过整流滤波及稳压DCDC，实现受电到超级电容充电，实现无线充电受电及储能。
![Charge](/img/Charge.jpg)
