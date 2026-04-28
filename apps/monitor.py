from cwio import *
from cwio.const import *
from machine import ADC
import time

name = "XIMonitor"
v_adc = ADC(3)

def get_v():
    t = 0
    for _ in range(20):
        t += v_adc.read_u16()
    return (t / 20) * (3.3 / 65535) * 3

def main():

    while True:
        v = get_v()
        p = ((v - 0.1) / (1.5 - 0.1)) * 100
        p = max(0, min(100, p))
        
        screen.clear()
        
        screen.write("BATT MONITOR", 40, 2, SCR.COLOR.BLACK, font.miniwi)
        
        screen.write(f"RAW VOLT: {v:.3f} V", 10, 20, SCR.COLOR.BLACK, font.miniwi)
        screen.write(f"PERCENT : {int(p)} %", 10, 30, SCR.COLOR.BLACK, font.miniwi)
        
        if v < 0.5:
            screen.write("CHECK WIRING!", 10, 45, SCR.COLOR.BLACK, font.miniwi)
        else:
            screen.write("SIGNAL OK", 10, 45, SCR.COLOR.BLACK, font.miniwi)

        screen.apply()
        
        if keyboard.pressed_any():
            if keyboard.get_next() == KB.KEY.HOME: return