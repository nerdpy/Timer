from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None #je to v countdown - abychom mohli použít i jinde

# ---------------------------- TIMER RESET ------------------------------- # 
def reset():
    """reset obrazovky"""
    window.after_cancel(timer) #zrušíme odpočet
    timer_label.config(text="Timer", fg=GREEN, bg=YELLOW)
    canvas.itemconfig(timer_text, text="00:00")
    global reps
    reps = 0
# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start():
    """spustí časovač"""
    global reps #abychom věděli počet opakování
    reps += 1
    work_sec = WORK_MIN * 60  #časy v sekundách, ať je můžeme použít dál
    short_sec = SHORT_BREAK_MIN * 60
    long_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0: #není to jenom 8, ale každý osmý
        countdown(long_sec)
        timer_label.config(text="Break", fg=RED)
    elif reps % 2 == 0:  #každá sudá  repetice (2,4,6,..) mimo dělitelnou 8
        countdown(short_sec)
        timer_label.config(text="Break", fg=PINK)
    else:
        countdown(work_sec) #všechny ostatní
        timer_label.config(text="Work", fg=GREEN)
        check_label.config(text="")


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def countdown(count):  #input číslo od kterého počítáme
    count_min = math.floor(count / 60)  #čas převede na minuty a nechá jen celé číslo  př.450sekund = 7min
    count_sec = count % 60  #zbytek sekund, které zůstaly po minutách 30sekund
     #zobrazuje to čas 5:0, ale chceme 5:00 =)
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")  #není to timer_text.config - není to label ale canvas
    if count > 0:
        global timer
        timer = window.after(1000, countdown, count - 1) #po 1000ms spustí countdown a začne odpočet
    else: # až dojede do 0, musí se spustit start() - ověří,jaká repetice a podle toho bude odpočet
        start()
        marks = ""
        work_session = math.floor(reps/2) #počet odpočtů - (work+break =  1 session)
        for _ in range(work_session):
            marks += "✔"
            check_label.config(text=marks) #po každé work session přidáme do label jeden check mark


# ---------------------------- GUI SETUP ------------------------------- #

window = Tk()  #máme importované *všechno z modulu
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)  #BG=BACKROUND


canvas = Canvas(width=210, height=230, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(106, 113, image=tomato_img)
timer_text = canvas.create_text(106, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

timer_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 45, "bold"))
timer_label.grid(column=1, row=0)

check_label = Label(bg=YELLOW, fg=GREEN)
check_label.grid(column=1, row=3)

start_button = Button(text="Start", command=start)
start_button.grid(column=0, row=2)
reset_button = Button(text="Reset", command=reset)
reset_button.grid(column=2, row=2)

window.mainloop()
