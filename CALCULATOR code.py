import tkinter as tk
from tkinter import font as tkfont
import math
import re

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        
        # Calculator state
        self.current_input = "0"
        self.previous_input = ""
        self.operation = None
        self.memory = 0
        self.reset_next_input = False
        
        # Custom fonts
        self.display_font = tkfont.Font(family="Helvetica", size=24)
        self.button_font = tkfont.Font(family="Helvetica", size=16)
        self.small_button_font = tkfont.Font(family="Helvetica", size=12)
        
        self.create_widgets()
        self.bind_keys()

    def create_widgets(self):
        # Display frame
        display_frame = tk.Frame(self.root, height=100)
        display_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Previous calculation display (smaller, top-aligned)
        self.previous_display = tk.Label(
            display_frame,
            text=self.previous_input,
            anchor="e",
            font=self.small_button_font,
            fg="gray"
        )
        self.previous_display.pack(expand=True, fill="both")
        
        # Current input display (larger, bottom-aligned)
        self.current_display = tk.Label(
            display_frame,
            text=self.current_input,
            anchor="e",
            font=self.display_font
        )
        self.current_display.pack(expand=True, fill="both")
        
        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Button layout
        buttons = [
            # Row 1: Memory functions and advanced operations
            ("MC", "MR", "M+", "M-", "C", "⌫"),
            # Row 2: Advanced math operations
            ("√", "x²", "x³", "x^y", "1/x", "±"),
            # Row 3: Numbers and basic operations
            ("7", "8", "9", "/", "%"),
            # Row 4: Numbers and basic operations
            ("4", "5", "6", "*", "!"),
            # Row 5: Numbers and basic operations
            ("1", "2", "3", "-", "π"),
            # Row 6: Numbers and basic operations
            ("0", ".", "=", "+", "e")
        ]
        
        # Create buttons
        for row_idx, row in enumerate(buttons):
            row_frame = tk.Frame(button_frame)
            row_frame.pack(expand=True, fill="both")
            
            for col_idx, button_text in enumerate(row):
                btn = tk.Button(
                    row_frame,
                    text=button_text,
                    font=self.button_font,
                    command=lambda text=button_text: self.on_button_click(text),
                    relief="ridge",
                    borderwidth=1
                )
                
                # Color coding
                if button_text in {"MC", "MR", "M+", "M-"}:
                    btn.config(bg="#e6e6e6", activebackground="#d4d4d4")
                elif button_text in {"C", "⌫"}:
                    btn.config(bg="#ff9999", activebackground="#ff8080")
                elif button_text in {"="}:
                    btn.config(bg="#99ccff", activebackground="#80b3ff")
                elif button_text in {"+", "-", "*", "/", "%", "x^y"}:
                    btn.config(bg="#f0f0f0", activebackground="#e0e0e0")
                elif button_text.isdigit() or button_text == ".":
                    btn.config(bg="#ffffff", activebackground="#f0f0f0")
                else:  # Advanced functions
                    btn.config(bg="#e6f3ff", activebackground="#d4e6f2")
                
                btn.pack(side="left", expand=True, fill="both", padx=2, pady=2)

    def bind_keys(self):
        # Number keys
        for num in "0123456789":
            self.root.bind(num, lambda event, text=num: self.on_button_click(text))
        
        # Operation keys
        self.root.bind("+", lambda event: self.on_button_click("+"))
        self.root.bind("-", lambda event: self.on_button_click("-"))
        self.root.bind("*", lambda event: self.on_button_click("*"))
        self.root.bind("/", lambda event: self.on_button_click("/"))
        self.root.bind("%", lambda event: self.on_button_click("%"))
        
        # Other keys
        self.root.bind(".", lambda event: self.on_button_click("."))
        self.root.bind("<Return>", lambda event: self.on_button_click("="))
        self.root.bind("<BackSpace>", lambda event: self.on_button_click("⌫"))
        self.root.bind("<Escape>", lambda event: self.on_button_click("C"))
        self.root.bind("c", lambda event: self.on_button_click("C"))
        self.root.bind("m", lambda event: self.on_button_click("M+"))
        self.root.bind("r", lambda event: self.on_button_click("MR"))

    def on_button_click(self, button_text):
        # Handle number input
        if button_text.isdigit():
            if self.current_input == "0" or self.reset_next_input:
                self.current_input = button_text
                self.reset_next_input = False
            else:
                self.current_input += button_text
        
        # Handle decimal point
        elif button_text == ".":
            if "." not in self.current_input:
                if self.reset_next_input:
                    self.current_input = "0."
                    self.reset_next_input = False
                else:
                    self.current_input += "."
        
        # Handle basic operations
        elif button_text in {"+", "-", "*", "/", "%", "x^y"}:
            if self.operation and not self.reset_next_input:
                self.calculate()
            self.previous_input = self.current_input
            self.operation = button_text
            self.reset_next_input = True
        
        # Handle equals
        elif button_text == "=":
            self.calculate()
            self.operation = None
            self.reset_next_input = True
        
        # Handle clear
        elif button_text == "C":
            self.current_input = "0"
            self.previous_input = ""
            self.operation = None
            self.reset_next_input = False
        
        # Handle backspace
        elif button_text == "⌫":
            if len(self.current_input) > 1:
                self.current_input = self.current_input[:-1]
            else:
                self.current_input = "0"
        
        # Handle sign change
        elif button_text == "±":
            if self.current_input.startswith("-"):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
        
        # Handle memory functions
        elif button_text == "MC":
            self.memory = 0
        elif button_text == "MR":
            self.current_input = str(self.memory)
            self.reset_next_input = False
        elif button_text == "M+":
            self.memory += float(self.current_input)
        elif button_text == "M-":
            self.memory -= float(self.current_input)
        
        # Handle advanced math operations
        elif button_text == "√":
            try:
                result = math.sqrt(float(self.current_input))
                self.current_input = self.format_result(result)
                self.reset_next_input = True
            except ValueError:
                self.current_input = "Error"
        elif button_text == "x²":
            result = float(self.current_input) ** 2
            self.current_input = self.format_result(result)
            self.reset_next_input = True
        elif button_text == "x³":
            result = float(self.current_input) ** 3
            self.current_input = self.format_result(result)
            self.reset_next_input = True
        elif button_text == "1/x":
            try:
                result = 1 / float(self.current_input)
                self.current_input = self.format_result(result)
                self.reset_next_input = True
            except ZeroDivisionError:
                self.current_input = "Error"
        elif button_text == "!":
            try:
                result = math.factorial(int(float(self.current_input)))
                self.current_input = self.format_result(result)
                self.reset_next_input = True
            except (ValueError, OverflowError):
                self.current_input = "Error"
        elif button_text == "π":
            if self.reset_next_input:
                self.current_input = str(math.pi)
            else:
                self.current_input += str(math.pi)
            self.reset_next_input = False
        elif button_text == "e":
            if self.reset_next_input:
                self.current_input = str(math.e)
            else:
                self.current_input += str(math.e)
            self.reset_next_input = False
        
        # Update display
        self.update_display()

    def calculate(self):
        try:
            num1 = float(self.previous_input)
            num2 = float(self.current_input)
            
            if self.operation == "+":
                result = num1 + num2
            elif self.operation == "-":
                result = num1 - num2
            elif self.operation == "*":
                result = num1 * num2
            elif self.operation == "/":
                result = num1 / num2
            elif self.operation == "%":
                result = num1 % num2
            elif self.operation == "x^y":
                result = num1 ** num2
            
            self.current_input = self.format_result(result)
            self.previous_input = ""
        except (ValueError, ZeroDivisionError):
            self.current_input = "Error"
            self.previous_input = ""
            self.operation = None

    def format_result(self, result):
        # Format result to remove unnecessary decimal places
        if result.is_integer():
            return str(int(result))
        else:
            # Limit to 10 decimal places to avoid floating point weirdness
            return "{0:.10f}".format(result).rstrip("0").rstrip(".")

    def update_display(self):
        # Update current display
        self.current_display.config(text=self.current_input)
        
        # Update previous display with operation if available
        if self.operation:
            prev_text = f"{self.previous_input} {self.operation}"
            self.previous_display.config(text=prev_text)
        else:
            self.previous_display.config(text=self.previous_input)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
