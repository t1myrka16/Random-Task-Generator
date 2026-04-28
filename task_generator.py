import tkinter as tk
import random
import json
import os

def load_tasks():
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        default = [
            {"name": "Прочитать статью", "type": "учёба"},
            {"name": "Сделать зарядку", "type": "спорт"},
            {"name": "Написать отчёт", "type": "работа"},
            {"name": "Выучить 10 новых слов", "type": "учёба"},
            {"name": "Пробежка 3 км", "type": "спорт"},
            {"name": "Провести совещание", "type": "работа"},
            {"name": "Посмотреть лекцию", "type": "учёба"},
            {"name": "Сделать растяжку", "type": "спорт"},
            {"name": "Закончить проект", "type": "работа"}
        ]
        save_tasks(default)
        return default

def save_tasks(tasks):
    with open("tasks.json", "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def load_history():
    if os.path.exists("history.json"):
        with open("history.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    with open("history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def update_task_display():
    history_listbox.delete(0, tk.END)
    
    filter_type = filter_var.get()
    
    filtered = []
    if filter_type == "все":
        filtered = history
    else:
        for item in history:
            if item["type"] == filter_type:
                filtered.append(item)
    
    for task in filtered:
        history_listbox.insert(tk.END, f"[{task['type']}] {task['name']}")

def generate_task():
    filter_type = filter_var.get()
    
    if filter_type == "все":
        available = tasks
    else:
        available = [t for t in tasks if t["type"] == filter_type]
    
    if not available:
        task_label.config(text="Нет задач выбранного типа!")
        return
    
    chosen = random.choice(available)
 
    history.append({"name": chosen["name"], "type": chosen["type"]})
    save_history(history)

    task_label.config(text=f"{chosen['name']} [{chosen['type']}]")

    update_task_display()

def add_task():
    name = task_entry.get().strip()
    task_type = type_var.get()
    
    if name == "":
        task_label.config(text="Ошибка: название не может быть пустым!")
        return
    
    tasks.append({"name": name, "type": task_type})
    save_tasks(tasks)
    
    task_entry.delete(0, tk.END)
    task_label.config(text=f"Задача '{name}' добавлена!")
    

def delete_last_task():
    if history:
        removed = history.pop()
        save_history(history)
        update_task_display()
        task_label.config(text=f"Удалено: {removed['name']}")
    else:
        task_label.config(text="История пуста!")

root = tk.Tk()
root.title("Random Task Generator")
root.geometry("550x550")
root.resizable(True, True)

tasks = load_tasks()
history = load_history()

frame_gen = tk.Frame(root, relief=tk.RAISED, borderwidth=2)
frame_gen.pack(fill=tk.X, padx=10, pady=5)

tk.Label(frame_gen, text="Текущая задача:", font=("Arial", 10, "bold")).pack(pady=(5,0))
task_label = tk.Label(frame_gen, text="Нажмите 'Сгенерировать'", 
                      font=("Arial", 12), fg="blue", wraplength=500)
task_label.pack(pady=5)

btn_generate = tk.Button(frame_gen, text="🎲 Сгенерировать задачу", 
                         command=generate_task, bg="lightgreen", font=("Arial", 10))
btn_generate.pack(pady=5)

frame_filter = tk.Frame(root, relief=tk.GROOVE, borderwidth=2)
frame_filter.pack(fill=tk.X, padx=10, pady=5)

tk.Label(frame_filter, text="Фильтр по типу:").pack(side=tk.LEFT, padx=5)

filter_var = tk.StringVar(value="все")
filter_all = tk.Radiobutton(frame_filter, text="Все", variable=filter_var, value="все", command=update_task_display)
filter_study = tk.Radiobutton(frame_filter, text="Учёба", variable=filter_var, value="учёба", command=update_task_display)
filter_sport = tk.Radiobutton(frame_filter, text="Спорт", variable=filter_var, value="спорт", command=update_task_display)
filter_work = tk.Radiobutton(frame_filter, text="Работа", variable=filter_var, value="работа", command=update_task_display)

filter_all.pack(side=tk.LEFT, padx=5)
filter_study.pack(side=tk.LEFT, padx=5)
filter_sport.pack(side=tk.LEFT, padx=5)
filter_work.pack(side=tk.LEFT, padx=5)

frame_add = tk.Frame(root, relief=tk.GROOVE, borderwidth=2)
frame_add.pack(fill=tk.X, padx=10, pady=5)

tk.Label(frame_add, text="Новая задача:").pack(side=tk.LEFT, padx=5)
task_entry = tk.Entry(frame_add, width=25)
task_entry.pack(side=tk.LEFT, padx=5)

tk.Label(frame_add, text="Тип:").pack(side=tk.LEFT, padx=5)
type_var = tk.StringVar(value="учёба")
type_menu = tk.OptionMenu(frame_add, type_var, "учёба", "спорт", "работа")
type_menu.pack(side=tk.LEFT, padx=5)

btn_add = tk.Button(frame_add, text="➕ Добавить", command=add_task, bg="lightyellow")
btn_add.pack(side=tk.LEFT, padx=5)

frame_history = tk.Frame(root)
frame_history.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

tk.Label(frame_history, text="История задач:", font=("Arial", 10, "bold")).pack(anchor=tk.W)

history_listbox = tk.Listbox(frame_history, height=12)
history_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

scrollbar = tk.Scrollbar(frame_history)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
history_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=history_listbox.yview)

frame_buttons = tk.Frame(root)
frame_buttons.pack(fill=tk.X, padx=10, pady=5)

btn_delete_last = tk.Button(frame_buttons, text="🗑 Удалить последнюю задачу из истории", 
                            command=delete_last_task, bg="lightcoral")
btn_delete_last.pack(side=tk.LEFT, padx=5)

def clear_all_history():
    global history
    history = []
    save_history(history)
    update_task_display()
    task_label.config(text="Вся история очищена!")

btn_clear_all = tk.Button(frame_buttons, text="❌ Очистить всю историю", 
                          command=clear_all_history, bg="orange")
btn_clear_all.pack(side=tk.LEFT, padx=5)

update_task_display()
root.mainloop()