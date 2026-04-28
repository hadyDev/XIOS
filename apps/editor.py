import machine
import ui
from cwio import *
from cwio.const import *

name = "XIViewer"

def main():
    file = ui.choose_file()
    if file == -1: return
    
    with open(file, "r") as f:
        l_lines = f.read().splitlines()
    if not l_lines: l_lines = [""]

    top = 0
    cx = 0
    cy = 0
    
    s_clear = screen.clear
    s_write = screen.write
    s_apply = screen.apply
    kb_pressed = keyboard.pressed_any
    kb_get = keyboard.get_next
    f_mini = font.miniwi
    color_b = SCR.COLOR.BLACK
    color_d = SCR.COLOR.DARK

    while True:
        s_clear()
        for i in range(8):
            idx = top + i
            if idx < len(l_lines):
                s_write(l_lines[idx], 0, i * 8, color_b, f_mini)
        
        curr_txt = l_lines[top + cy]
        actual_cx = cx if cx <= len(curr_txt) else len(curr_txt)
        s_write("|", actual_cx * 4, cy * 8, color_d, f_mini)
        s_apply()

        if not kb_pressed():
            pass
            
        key = kb_get()
        
        if key == KB.KEY.DOWN:
            if cy < 7:
                if (top + cy) < len(l_lines) - 1: cy += 1
            elif (top + cy) < len(l_lines) - 1:
                top += 1

        elif key == KB.KEY.UP:
            if cy > 0: cy -= 1
            elif top > 0: top -= 1

        elif key == KB.KEY.LEFT:
            if cx > 0: cx -= 1

        elif key == KB.KEY.RIGHT:
            if cx < len(l_lines[top + cy]): cx += 1

        elif key == KB.KEY.BKSPACE:
            idx = top + cy
            if cx > 0:
                l_lines[idx] = l_lines[idx][:cx-1] + l_lines[idx][cx:]
                cx -= 1
            elif idx > 0:
                cx = len(l_lines[idx-1])
                l_lines[idx-1] += l_lines.pop(idx)
                if cy > 0: cy -= 1
                else: top -= 1

        elif key == KB.KEY.EXE:
            idx = top + cy
            l_lines.insert(idx + 1, l_lines[idx][cx:])
            l_lines[idx] = l_lines[idx][:cx]
            cx = 0
            if cy < 7: cy += 1
            else: top += 1

        elif key == KB.KEY.HOME:
            return