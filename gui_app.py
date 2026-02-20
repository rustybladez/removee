import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from rembg import remove
from PIL import Image, ImageTk
import os
import threading
import time

selected_file = None
processing_done = False


def select_file():
    global selected_file

    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.webp")]
    )

    if not file_path:
        return

    selected_file = file_path
    status_label.config(text=os.path.basename(file_path))

    img = Image.open(file_path)
    img.thumbnail((350, 350))
    tk_img = ImageTk.PhotoImage(img)

    original_preview.config(image=tk_img)
    original_preview.image = tk_img

    result_preview.config(image="")
    result_preview.image = None


def start_processing():
    global processing_done

    if not selected_file:
        messagebox.showerror("Error", "Please select an image first.")
        return

    processing_done = False
    progress["value"] = 0

    threading.Thread(target=remove_background, daemon=True).start()
    threading.Thread(target=simulate_progress, daemon=True).start()


def simulate_progress():
    while not processing_done and progress["value"] < 95:
        progress["value"] += 1
        time.sleep(0.02)

    # Wait until actual processing finishes
    while not processing_done:
        time.sleep(0.01)

    # Smooth finish to 100%
    while progress["value"] < 100:
        progress["value"] += 1
        time.sleep(0.01)


def remove_background():
    global processing_done

    try:
        status_label.config(text="Processing...")

        with Image.open(selected_file) as img:
            result = remove(img)

        filename, _ = os.path.splitext(selected_file)
        output_path = f"{filename}_no_bg.png"
        result.save(output_path)

        result_display = result.copy()
        result_display.thumbnail((350, 350))
        tk_result = ImageTk.PhotoImage(result_display)

        result_preview.config(image=tk_result)
        result_preview.image = tk_result

        status_label.config(text="Done")
        messagebox.showinfo("Success", f"Saved to:\n{output_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        processing_done = True


# ---------------- UI ---------------- #

root = tk.Tk()
root.title("Private Background Remover")
root.geometry("900x600")
root.configure(bg="#ffffff")

title_label = tk.Label(
    root,
    text="Private Background Remover",
    font=("Segoe UI", 18, "bold"),
    bg="#ffffff",
)
title_label.pack(pady=(20, 10))

controls_frame = tk.Frame(root, bg="#ffffff")
controls_frame.pack(pady=10)

select_button = tk.Button(
    controls_frame,
    text="Select Image",
    command=select_file,
    bg="#e5e5e5",
    relief="flat",
    padx=15,
    pady=6,
)
select_button.grid(row=0, column=0, padx=10)

remove_button = tk.Button(
    controls_frame,
    text="Remove Background",
    command=start_processing,
    bg="#4CAF50",
    fg="white",
    relief="flat",
    padx=15,
    pady=6,
)
remove_button.grid(row=0, column=1, padx=10)

status_label = tk.Label(
    root,
    text="No file selected",
    font=("Segoe UI", 10, "italic"),
    bg="#ffffff",
)
status_label.pack(pady=(5, 5))

progress = ttk.Progressbar(
    root,
    mode="determinate",
    length=300,
    maximum=100
)
progress.pack(pady=(0, 15))

preview_frame = tk.Frame(root, bg="#ffffff")
preview_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)

left_container = tk.Frame(preview_frame, bg="#ffffff")
left_container.pack(side=tk.LEFT, expand=True)

tk.Label(
    left_container,
    text="Original",
    font=("Segoe UI", 12, "bold"),
    bg="#ffffff",
).pack(pady=5)

original_preview = tk.Label(
    left_container,
    bg="#f2f2f2",
    width=350,
    height=350,
)
original_preview.pack(padx=20, pady=10)

right_container = tk.Frame(preview_frame, bg="#ffffff")
right_container.pack(side=tk.LEFT, expand=True)

tk.Label(
    right_container,
    text="Result (No Background)",
    font=("Segoe UI", 12, "bold"),
    bg="#ffffff",
).pack(pady=5)

result_preview = tk.Label(
    right_container,
    bg="#f2f2f2",
    width=350,
    height=350,
)
result_preview.pack(padx=20, pady=10)

root.mainloop()