import random
import threading
import time
import tkinter as tk

import keyboard
import mouse

is_enabled = True
click_event = threading.Event()
initial_x, initial_y = 0, 0

APP_TITLE = "Автоклікер"

def toggle_enable():
    global is_enabled, initial_x, initial_y
    is_enabled = not is_enabled
    if not is_enabled:
        entry1.configure(state="disabled")
        entry2.configure(state="disabled")
        entry3.configure(state="disabled")
        reset_button.configure(state="disabled")
        click_event.set()
        console_label.config(text="Автоклікер увімкнено. Щоб вимкнути, натисніть ctrl+alt+b.")
        initial_x, initial_y = mouse.get_position()
        print("Увімкнено")
    else:
        entry1.configure(state="normal")
        entry2.configure(state="normal")
        entry3.configure(state="normal")
        reset_button.configure(state="normal")
        click_event.clear()
        console_label.config(text="Автоклікер вимкнено. Щоб увімкнути, натисніть ctrl+alt+b.\n"
                                  "Перед натисканням переконайтеся, що курсор миші знаходиться на об'єкті, на який потрібно клікати!")
        print(f"Вимкнено: {entry1.get()}")

def enforce_range(entry_widget):
    try:
        value = entry_widget.get().lstrip("0") or "0"
        if value == "":
            value = "0"
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, str(float(value)))
        value = float(entry_widget.get())
        if value < 0:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, "0.01")
        elif value > 1:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, "1.0")
    except ValueError:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, "0.01")

def validate_input(new_value):
    if new_value == "" or new_value == ".":
        return True
    try:
        value = float(new_value)
        return 0 <= value <= 1
    except ValueError:
        return False

def reset_defaults():
    if is_enabled:
        entry1.delete(0, tk.END)
        entry1.insert(0, "0.05")
        entry2.delete(0, tk.END)
        entry2.insert(0, "0.17")
        entry3.delete(0, tk.END)
        entry3.insert(0, "0.2")

def keyboard_listener():
    while True:
        keyboard.wait("ctrl+alt+b")
        toggle_enable()

def click():
    global initial_x, initial_y
    while True:
        click_event.wait()
        val = max(1, int(float(entry3.get()) * 10))
        random_offset_x = random.randint(-val, val)
        random_offset_y = random.randint(-val, val)
        new_x = initial_x + random_offset_x
        new_y = initial_y + random_offset_y
        mouse.move(new_x, new_y, absolute=True, duration=0.01)
        print("AAA")
        mouse.double_click(button='left')
        str_val = float(entry2.get())
        time.sleep(round(random.uniform(max(0.01, float(entry1.get())), max(0.02, str_val)), 5))

def main():
    global entry1, entry2, entry3, console_label, reset_button
    root = tk.Tk()
    root.title(APP_TITLE)
    root.geometry("640x520")
    tk.Label(root, text=APP_TITLE, font=("Arial", 14, "bold"), fg="blue").pack(pady=10)
    tk.Label(root, text="⚠ Усі значення налаштовані для мінімізації ризику бана", fg="red").pack(pady=10)
    validate_cmd = root.register(validate_input)

    tk.Label(root, text="Інтервал між кліками (секунди):", anchor="w").pack(pady=2)
    entry1 = tk.Entry(root, width=10, validate="key", validatecommand=(validate_cmd, '%P'))
    entry1.insert(0, "0.05")
    entry1.pack(pady=2)
    entry1.bind("<FocusOut>", lambda event: enforce_range(entry1))

    tk.Label(root, text="Максимальний інтервал між кліками (секунди):", anchor="w").pack(pady=2)
    entry2 = tk.Entry(root, width=10, validate="key", validatecommand=(validate_cmd, '%P'))
    entry2.insert(0, "0.17")
    entry2.pack(pady=2)
    entry2.bind("<FocusOut>", lambda event: enforce_range(entry2))

    tk.Label(root, text="Діапазон випадкового зміщення (пікселі):", anchor="w").pack(pady=2)
    entry3 = tk.Entry(root, width=10, validate="key", validatecommand=(validate_cmd, '%P'))
    entry3.insert(0, "0.2")
    entry3.pack(pady=2)
    entry3.bind("<FocusOut>", lambda event: enforce_range(entry3))

    reset_button = tk.Button(root, text="Скинути параметри", command=reset_defaults)
    reset_button.pack(pady=10)

    console_label = tk.Label(root, text="", fg="green")
    console_label.pack(pady=10)
    console_label.config(text="Автоклікер вимкнено. Щоб увімкнути, натисніть ctrl+alt+b.\n"
                              "Перед натисканням переконайтеся, що курсор миші знаходиться на об'єкті, на який потрібно клікати!")

    threading.Thread(target=keyboard_listener, daemon=True).start()
    threading.Thread(target=click, daemon=True).start()

    root.mainloop()


if __name__ == '__main__':
    main()
