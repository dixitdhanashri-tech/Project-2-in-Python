import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
import math

FONT = ('Arial', 9,)
try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    HAS_MPL = True
except Exception:
    HAS_MPL = False


class ProfessionalCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title('All in One Calculator')
        self.root.geometry('490x480')
        self.root.minsize(500, 400)
        self.root.configure(bg='#0F4C81')
        self.root.option_add('*Font', FONT)
        self.root.option_add('*TCombobox*Listbox.font', FONT)
        self.history = []
        self.history_text_boxes = []
        self.expr = tk.StringVar()

        self.menu = tk.Frame(root, bg='#1E5FAF', width=118)
        self.menu.pack(side='left', fill='y')
        self.menu.pack_propagate(False)
        self.content = tk.Frame(root, bg='#0F4C81')
        self.content.pack(side='right', fill='both', expand=True)

        tk.Label(self.menu, text='CALCULATOR', bg='#1E5FAF', fg='white',
                 font=FONT).pack(pady=(10, 8))
        pages = [('Standard', self.standard), ('Scientific', self.scientific),
                 ('BMI Calculator', self.bmi), ('Age Calculator', self.age),
                 ('Graph Calculator', self.graph), ('Unit Converter', self.converter)]
        for label, command in pages:
            tk.Button(self.menu, text=label, font=FONT,
                      bg='white', fg='black', command=command).pack(
                          padx=6, pady=3, fill='x', ipady=4)
        tk.Button(self.menu, text='Exit', font=FONT, bg='white', fg='black',
                  command=self.exit_calculator).pack(
                      side='bottom', padx=6, pady=8, fill='x', ipady=4)
        self.standard()

    def clear_page(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def page_title(self, title):
        tk.Label(self.content, text=title, font=FONT,
                 bg='#0F4C81', fg='white').pack(pady=8)

    def evaluate(self):
        expression = self.expr.get().strip()
        # Accept common typed math symbols as well as keypad syntax.
        expression = expression.replace('×', '*').replace('÷', '/').replace('−', '-').replace('^', '**')
        if not expression:
            return
        try:
            allowed = {name: getattr(math, name) for name in dir(math) if not name.startswith('_') and name not in {'asin', 'acos', 'atan', 'exp'}}
            result = eval(expression, {'__builtins__': {}}, allowed)
            result_text = str(result)
            self.history.append(f'{expression} = {result_text}')
            self.refresh_history_views()
            self.expr.set(result_text)
        except Exception as exc:
            messagebox.showerror('Calculation Error', f'Invalid expression.\n{exc}')

    def show_history(self):
        popup = tk.Toplevel(self.root)
        popup.title('Calculation History')
        popup.geometry('480x360')
        popup.configure(bg='#0F4C81')
        tk.Label(popup, text='Calculation History', font=FONT,
                 bg='#0F4C81', fg='white').pack(pady=8)
        frame = tk.Frame(popup)
        frame.pack(fill='both', expand=True, padx=12, pady=8)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side='right', fill='y')
        text_box = tk.Text(frame, wrap='word', font=FONT,
                           yscrollcommand=scrollbar.set)
        text_box.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=text_box.yview)
        text_box.insert('1.0', '\n'.join(self.history[-100:]) if self.history else 'No calculation history yet.')
        text_box.config(state='disabled')
        self.history_text_boxes.append(text_box)
        tk.Button(popup, text='Close', bg='white', command=popup.destroy).pack(pady=8)

    def refresh_history_views(self):
        display_text = '\n'.join(self.history[-100:]) if self.history else 'No calculation history yet.'
        active_boxes = []
        for text_box in self.history_text_boxes:
            if text_box.winfo_exists():
                text_box.config(state='normal')
                text_box.delete('1.0', 'end')
                text_box.insert('1.0', display_text)
                text_box.config(state='disabled')
                active_boxes.append(text_box)
        self.history_text_boxes = active_boxes

    def delete_history(self):
        self.history.clear()
        self.refresh_history_views()
        messagebox.showinfo('History', 'All calculation history has been deleted.')

    def exit_calculator(self):
        if messagebox.askyesno('Exit Calculator', 'Are you sure you want to exit?'):
            self.root.destroy()

    def build_calculator(self, scientific=False):
        self.clear_page()
        self.page_title('Scientific Calculator' if scientific else 'Standard Calculator')
        tk.Label(self.content, text='Type an expression or use the keypad', font=FONT, bg='#0F4C81', fg='white').pack(pady=(2, 0))
        entry = tk.Entry(self.content, textvariable=self.expr, font=FONT, justify='right')
        entry.pack(fill='x', padx=12, pady=5)
        entry.bind('<Return>', lambda event: self.evaluate())
        top = tk.Frame(self.content, bg='#0F4C81')
        top.pack(fill='x', padx=8, pady=3)
        tk.Button(top, text='Show History', font=FONT, bg='white', command=self.show_history).pack(side='left', padx=4)
        tk.Button(top, text='Delete History', font=FONT, bg='white', command=self.delete_history).pack(side='left', padx=4)
        tk.Button(top, text='Clear', font=FONT, bg='white', command=lambda: self.expr.set('')).pack(side='right', padx=4)

        pad = tk.Frame(self.content, bg='#0F4C81')
        pad.pack(expand=True, pady=8)
        if scientific:
            keys = [['sin(', 'cos(', 'tan(', 'sqrt(', 'log('],
                    ['7', '8', '9', '/', '('], ['4', '5', '6', '*', ')'],
                    ['1', '2', '3', '-', '**'], ['0', '.', '%', '+', '=']]
        else:
            keys = [['7', '8', '9', '/'], ['4', '5', '6', '*'],
                    ['1', '2', '3', '-'], ['0', '.', '(', ')'], ['%', '**', '+', '=']]
        for r, row in enumerate(keys):
            for c, key in enumerate(row):
                def command(value=key):
                    if value == '=':
                        self.evaluate()
                    else:
                        self.expr.set(self.expr.get() + value)
                        entry.focus_set()
                tk.Button(pad, text=key, font=FONT, bg='white',
                          width=9 if scientific else 10, height=2, command=command).grid(
                              row=r, column=c, padx=3, pady=3, sticky='nsew')

    def standard(self):
        self.build_calculator(False)

    def scientific(self):
        self.build_calculator(True)

    def bmi(self):
        self.clear_page()
        self.page_title('BMI Calculator')
        form = tk.Frame(self.content, bg='#0F4C81')
        form.pack(expand=True)
        tk.Label(form, text='Weight (kg)', font=FONT, bg='#0F4C81', fg='white').grid(row=0, column=0, padx=10, pady=10, sticky='e')
        weight = tk.Entry(form, font=FONT, justify='center', width=20)
        weight.grid(row=0, column=1, padx=10, pady=10)
        tk.Label(form, text='Height (cm)', font=FONT, bg='#0F4C81', fg='white').grid(row=1, column=0, padx=10, pady=10, sticky='e')
        height = tk.Entry(form, font=FONT, justify='center', width=20)
        height.grid(row=1, column=1, padx=10, pady=10)
        output = tk.Label(form, text='', font=FONT, bg='#0F4C81', fg='white')
        output.grid(row=3, column=0, columnspan=2, pady=15)

        def calculate():
            try:
                kg, cm = float(weight.get()), float(height.get())
                if kg <= 0 or cm <= 0:
                    raise ValueError
                value = kg / (cm / 100) ** 2
                category = 'Underweight' if value < 18.5 else 'Normal weight' if value < 25 else 'Overweight' if value < 30 else 'Obesity'
                output.config(text=f'BMI: {value:.2f}\nCategory: {category}')
            except ValueError:
                messagebox.showerror('Input Error', 'Enter valid positive numbers for weight and height.')
        tk.Button(form, text='Calculate BMI', bg='white', font=FONT, command=calculate).grid(row=2, column=0, columnspan=2, pady=8)

    def age(self):
        self.clear_page()
        self.page_title('Age Calculator')
        form = tk.Frame(self.content, bg='#0F4C81')
        form.pack(expand=True)
        tk.Label(form, text='Date of Birth (DD/MM/YYYY)', font=FONT, bg='#0F4C81', fg='white').pack(pady=8)
        entry = tk.Entry(form, font=FONT, justify='center', width=22)
        entry.pack(pady=6)
        output = tk.Label(form, text='', bg='#0F4C81', fg='white', font=FONT)
        output.pack(pady=8)

        def calculate():
            try:
                birth = datetime.strptime(entry.get().strip(), '%d/%m/%Y').date()
                today = date.today()
                if birth > today:
                    raise ValueError
                years = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
                output.config(text=f'Age: {years} years')
            except ValueError:
                messagebox.showerror('Input Error', 'Enter a valid date in DD/MM/YYYY format, not in the future.')
        tk.Button(form, text='Calculate Age', bg='white', font=FONT, command=calculate).pack(pady=8)

    def graph(self):
        self.clear_page()
        self.page_title('Scientific Graph Calculator')
        if not HAS_MPL:
            tk.Label(self.content, text='Install matplotlib to use graph plotting:\npip install matplotlib', bg='#0F4C81', fg='white').pack(pady=20)
            return
        controls = tk.Frame(self.content, bg='#0F4C81')
        controls.pack(fill='x', padx=12)
        tk.Label(controls, text='X-axis values (comma-separated)', bg='#0F4C81', fg='white').grid(row=0, column=0, sticky='w', padx=4, pady=4)
        x_entry = tk.Entry(controls, font=FONT, width=24)
        x_entry.grid(row=0, column=1, padx=4, pady=4)
        tk.Label(controls, text='Y-axis values (comma-separated)', bg='#0F4C81', fg='white').grid(row=1, column=0, sticky='w', padx=4, pady=4)
        y_entry = tk.Entry(controls, font=FONT, width=24)
        y_entry.grid(row=1, column=1, padx=4, pady=4)
        tk.Label(controls, text='Chart type', bg='#0F4C81', fg='white').grid(row=2, column=0, sticky='w', padx=4, pady=4)
        chart_type = tk.StringVar(value='Bar')
        ttk.Combobox(controls, textvariable=chart_type, state='readonly',
                     values=['Bar', 'Column', 'Histogram', 'Pie', 'Box Plot'], width=18).grid(row=2, column=1, sticky='w', padx=4, pady=4)
        fig = Figure(figsize=(4.2, 2.5), dpi=90)
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, self.content)
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=5)

        def plot():
            try:
                xs = [v.strip() for v in x_entry.get().split(',') if v.strip()]
                ys = [float(v.strip()) for v in y_entry.get().split(',') if v.strip()]
                kind = chart_type.get()
                ax.clear()
                if kind == 'Histogram':
                    if not ys:
                        raise ValueError('Enter numeric Y-axis values for the histogram.')
                    ax.hist(ys)
                elif kind == 'Box Plot':
                    if not ys:
                        raise ValueError('Enter numeric Y-axis values for the box plot.')
                    ax.boxplot(ys)
                elif kind == 'Pie':
                    if len(xs) != len(ys) or not ys or any(v < 0 for v in ys) or sum(ys) <= 0:
                        raise ValueError('Pie chart needs matching X labels and non-negative Y values with a positive total.')
                    ax.pie(ys, labels=xs, autopct='%1.1f%%')
                else:
                    if len(xs) != len(ys) or not ys:
                        raise ValueError('Enter the same number of X labels and Y values.')
                    if kind == 'Column':
                        ax.bar(xs, ys)
                    else:
                        ax.barh(xs, ys)
                    ax.set_xlabel('X-axis')
                    ax.set_ylabel('Y-axis')
                if kind in ('Histogram', 'Box Plot'):
                    ax.set_xlabel('Values')
                    ax.set_ylabel('Frequency' if kind == 'Histogram' else 'Distribution')
                ax.set_title(kind + ' Chart')
                fig.tight_layout()
                canvas.draw()
            except Exception as exc:
                messagebox.showerror('Graph Input Error', str(exc))
        tk.Button(self.content, text='Plot Graph', bg='white', font=FONT, command=plot).pack(pady=5)

    def converter(self):
        self.clear_page()
        self.page_title('Unit Converter')
        categories = {
            'Length': {'Meter': 1, 'Kilometer': 1000, 'Centimeter': 0.01, 'Millimeter': 0.001, 'Mile': 1609.344, 'Foot': 0.3048, 'Inch': 0.0254},
            'Volume': {'Liter': 1, 'Milliliter': 0.001, 'Cubic meter': 1000, 'Gallon (US)': 3.785411784},
            'Energy': {'Joule': 1, 'Kilojoule': 1000, 'Calorie': 4.184, 'Kilowatt-hour': 3600000},
            'Area': {'Square meter': 1, 'Square kilometer': 1000000, 'Square centimeter': 0.0001, 'Hectare': 10000, 'Acre': 4046.8564224},
            'Speed': {'Meter/second': 1, 'Kilometer/hour': 1/3.6, 'Mile/hour': 0.44704, 'Knot': 0.514444},
            'Time': {'Second': 1, 'Minute': 60, 'Hour': 3600, 'Day': 86400},
        }
        frame = tk.Frame(self.content, bg='#0F4C81')
        frame.pack(expand=True)
        category = tk.StringVar(value='Length')
        source = tk.StringVar(value='Meter')
        target = tk.StringVar(value='Kilometer')
        amount = tk.Entry(frame, font=FONT, justify='center', width=22)
        amount.insert(0, '1')
        result = tk.Label(frame, text='Converted value will appear here', font=FONT, bg='#0F4C81', fg='white')

        def unit_list(*_):
            if category.get() == 'Temperature':
                units = ['Celsius', 'Fahrenheit', 'Kelvin']
            else:
                units = list(categories[category.get()].keys())
            from_box['values'] = units
            to_box['values'] = units
            source.set(units[0])
            target.set(units[1] if len(units) > 1 else units[0])

        tk.Label(frame, text='Conversion category', bg='#0F4C81', fg='white', font=FONT).pack(pady=(5, 3))
        category_box = ttk.Combobox(frame, textvariable=category, state='readonly', values=['Length', 'Volume', 'Temperature', 'Energy', 'Area', 'Speed', 'Time'], width=25)
        category_box.pack(pady=5)
        category_box.bind('<<ComboboxSelected>>', unit_list)
        tk.Label(frame, text='Enter value', bg='#0F4C81', fg='white').pack(pady=(12, 3))
        amount.pack(pady=4)
        tk.Label(frame, text='From unit', bg='#0F4C81', fg='white').pack(pady=(8, 3))
        from_box = ttk.Combobox(frame, textvariable=source, state='readonly', width=25)
        from_box.pack(pady=4)
        tk.Label(frame, text='To unit', bg='#0F4C81', fg='white').pack(pady=(8, 3))
        to_box = ttk.Combobox(frame, textvariable=target, state='readonly', width=25)
        to_box.pack(pady=4)
        result.pack(pady=15)

        def convert():
            try:
                value = float(amount.get())
                if category.get() == 'Temperature':
                    c = {'Celsius': value, 'Fahrenheit': (value - 32) * 5 / 9, 'Kelvin': value - 273.15}[source.get()]
                    converted = {'Celsius': c, 'Fahrenheit': c * 9 / 5 + 32, 'Kelvin': c + 273.15}[target.get()]
                else:
                    units = categories[category.get()]
                    converted = value * units[source.get()] / units[target.get()]
                result.config(text=f'{value:g} {source.get()} = {converted:.6g} {target.get()}')
            except (ValueError, KeyError, ZeroDivisionError):
                messagebox.showerror('Conversion Error', 'Please enter a valid number and select units.')
        tk.Button(frame, text='Convert', bg='white', font=FONT, command=convert).pack(pady=8)
        unit_list()


if __name__ == '__main__':
    root = tk.Tk()
    app = ProfessionalCalculator(root)
    root.mainloop()


