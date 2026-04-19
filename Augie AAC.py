from machine import Pin, PWM, I2C
import time

# ---------- LEDS ----------
# physical pin 21 = GP16
# physical pin 22 = GP17
# physical pin 24 = GP18
green = Pin(16, Pin.OUT)
yellow = Pin(17, Pin.OUT)
red = Pin(18, Pin.OUT)

# ---------- BUZZER ----------
# buzzer negative on physical pin 5 = GP3
buzzer = PWM(Pin(3))
buzzer.duty_u16(0)

# ---------- ULTRASONIC ----------
# TRIG on physical pin 19 = GP14
# ECHO on physical pin 20 = GP15
trig = Pin(14, Pin.OUT)
echo = Pin(15, Pin.IN)

# ---------- MPU6050 ----------
# SCL on physical pin 7 = GP5
# SDA on physical pin 6 = GP4
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)
MPU_ADDR = 0x68

# wake up MPU6050
i2c.writeto_mem(MPU_ADDR, 0x6B, b'\x00')

def read_word(addr):
    high = i2c.readfrom_mem(MPU_ADDR, addr, 1)[0]
    low = i2c.readfrom_mem(MPU_ADDR, addr + 1, 1)[0]
    value = (high << 8) | low
    if value > 32767:
        value -= 65536
    return value

def read_accel():
    ax = read_word(0x3B)
    ay = read_word(0x3D)
    az = read_word(0x3F)
    return ax, ay, az

def get_distance():
    trig.low()
    time.sleep_us(2)
    trig.high()
    time.sleep_us(10)
    trig.low()

    timeout_us = 30000

    start_wait = time.ticks_us()
    while echo.value() == 0:
        if time.ticks_diff(time.ticks_us(), start_wait) > timeout_us:
            return None

    start = time.ticks_us()

    while echo.value() == 1:
        if time.ticks_diff(time.ticks_us(), start) > timeout_us:
            return None

    end = time.ticks_us()
    duration = time.ticks_diff(end, start)
    return duration * 0.0343 / 2

def beep(freq, on_time, off_time=0):
    buzzer.freq(freq)
    buzzer.duty_u16(30000)
    time.sleep(on_time)
    buzzer.duty_u16(0)
    if off_time > 0:
        time.sleep(off_time)

prev_ax, prev_ay, prev_az = read_accel()
last_fall_time = 0

while True:
    try:
        d = get_distance()
        ax, ay, az = read_accel()

        change = abs(ax - prev_ax) + abs(ay - prev_ay) + abs(az - prev_az)

        prev_ax, prev_ay, prev_az = ax, ay, az

        print("Distance:", round(d, 1) if d is not None else None, "| Motion:", change)

        now = time.ticks_ms()

        # ---------- FALL / STRONG SHOCK ----------
        if change > 12000 and time.ticks_diff(now, last_fall_time) > 1500:
            time.sleep(0.08)
            ax2, ay2, az2 = read_accel()
            change2 = abs(ax2 - ax) + abs(ay2 - ay) + abs(az2 - az)

            if change2 > 30000:
                print("FALL / STRONG SHOCK DETECTED")
                last_fall_time = now
                for _ in range(3):
                    green.value(0)
                    yellow.value(0)
                    red.value(1)
                    beep(2200, 0.15, 0.05)
                    red.value(0)
                    time.sleep(0.05)
                continue

      
            # ---------- DISTANCE / LED LOGIC ----------
        if d is None:
            green.value(1)
            yellow.value(0)
            red.value(0)
            buzzer.duty_u16(0)
            time.sleep(0.05)

        elif d < 35:
            green.value(0)
            yellow.value(0)
            red.value(1)
            buzzer.freq(2500)
            buzzer.duty_u16(35000)
            time.sleep(0.1)

        elif d < 70:
            green.value(0)
            yellow.value(1)
            red.value(0)
            beep(2000, 0.07, 0.07)

        elif d < 120:
            green.value(1)
            yellow.value(0)
            red.value(0)
            beep(1200, 0.12, 0.5)

        else:
            green.value(1)
            yellow.value(0)
            red.value(0)
            buzzer.duty_u16(0)
            time.sleep(0.05)
      
 

    except OSError:
        print("MPU read error - connection moved too much")
        green.value(1)
        yellow.value(0)
        red.value(0)
        buzzer.duty_u16(0)
        time.sleep(0.1)