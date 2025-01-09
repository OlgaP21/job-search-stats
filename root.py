import tkinter as tk
from tkinter import ttk
from tkinter import font
from data import Data
from stats import Stats


class Root(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.style = Style(self)
        self.geometry('1020x670')
        self.resizable(False, False)
        self.title('My Job Search Stats')
        self._notebook = TabControl(self)


class Style(ttk.Style):
    
    def __init__(self, parent):
        ttk.Style.__init__(self, parent)
        self.theme_use('clam')
        self.configure('TNotebook.Tab', width=21)
        self.configure('TEntry', padding=[10, 5, 10, 5])


class TabControl(ttk.Notebook):
    
    _tab_names = [
        f'{" "*10}Lisa uus kirjend',
        f'{" "*14}CVKeskus',
        f'{" "*18}cv.ee',
        f'{" "*13}Töötukassa',
        f'{" "*19}E-kiri',
        f'{" "*19}Muu',
        f'{" "*19}Stats'
    ]
    notebook_tabs = []
    
    def __init__(self, parent):
        ttk.Notebook.__init__(self, parent)
        self._add_tabs()
        self.grid(row=0, column=0, sticky='nsew')
    
    
    def _add_tabs(self):
        for i, tab_name in enumerate(self._tab_names):
            if i == 0:
                tab = TabAdd(self)
            elif i == len(self._tab_names)-1:
                tab = TabStats(self)
            else:
                tab = Tab(self, tab_name.strip())
            self.add(tab, text=tab_name)
            self.notebook_tabs.append(tab)
    
    
    def _get_tab_index(self, source_tab: str) -> int:
        for i in range(len(self._tab_names)):
            if source_tab in self._tab_names[i]:
                return i
    
    
    def add_to_tab(self, source_tab: str, application_data: list[str]) -> None:
        index = self._get_tab_index(source_tab)
        self.notebook_tabs[index].add_application(application_data)
    
    
    def update_statistics(self):
        self.notebook_tabs[-1].update_stats()


class Tab(ttk.Frame):
    
    def __init__(self, parent, name):
        ttk.Frame.__init__(self, parent)
        self.grid(row=0, column=0, sticky='nsew')
        self._table = Tree(self, name)
        self._parent = parent
        self._scrollbar = Scroll(self, self._table)
        self._table.configure(yscroll=self._scrollbar.set)
    
    
    def add_application(self, application_data: list[str]) -> None:
        self._table.add_new_entry(application_data)
    
    
    def update_stats(self):
        self._parent.update_statistics()


class TabAdd(ttk.Frame):
    
    _dropdown_menu_names = ['source', 'day', 'month', 'year', 'status']
    _input_field_names = ['title', 'company']
    
    _dropdown_menus = []
    _input_fields = []
    
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.grid(row=0, column=0, sticky='nsew')
        self._parent = parent
        self._add_dropdown_menus()
        self._add_input_fields()
        self._add_button()
    
    
    def _add_dropdown_menus(self):
        for name in self._dropdown_menu_names:
            dropdown_menu = DropdownMenu(self, name)
            self._dropdown_menus.append(dropdown_menu)
    
    
    def _add_input_fields(self):
        for name in self._input_field_names:
            input_field = InputField(self, name)
            self._input_fields.append(input_field)
    
    
    def _add_button(self):
        self._button = ttk.Button(self, text='Lisa', command=self._add_entry)
        self._button.grid(row=3, column=0, columnspan=5, sticky='nsew', padx=90, pady=30)
    
    
    def _add_entry(self):
        source = self._dropdown_menus[0].get_selected()
        day = self._dropdown_menus[1].get_selected()
        month = self._dropdown_menus[2].get_selected()
        year = self._dropdown_menus[3].get_selected()
        status = self._dropdown_menus[4].get_selected()
        title = self._input_fields[0].get_text()
        company = self._input_fields[1].get_text()
        application_data = Data.add_entry([source, day, month, year, title, company, status])
        self._parent.add_to_tab(source, application_data)
        self._parent.update_statistics()


class TabStats(ttk.Frame):
    _sources = ['Kokku', 'CVKeskus', 'cv.ee', 'Töötukassa', 'E-kiri', 'Muu']
    _labels = []
    
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.grid(row=0, column=0, sticky='nsew')
        self._add_stats()
    
    
    def _add_stats(self):
        _index = 0
        for source in self._sources:
            total_n, responded_n, not_responded_n, tbd_n = Stats.get_numbers(source)
            total_p, responded_p, not_responded_p, tbd_p = Stats.get_percent(source)
            self._labels.append(TextLabel(self, source, _index))
            self._labels.append(TextLabel(self, f'Taotlusi {total_n} ({total_p}%)', _index+1))
            self._labels.append(TextLabel(self, f'Vastusega {responded_n} ({responded_p}%)', _index+2))
            self._labels.append(TextLabel(self, f'Vastuseta {not_responded_n} ({not_responded_p}%)', _index+3))
            self._labels.append(TextLabel(self, f'TBD {tbd_n} ({tbd_p}%)', _index+4))
            _index += 5
    
    
    def update_stats(self):
        _index = 0
        for source in self._sources:
            total_n, responded_n, not_responded_n, tbd_n = Stats.get_numbers(source)
            total_p, responded_p, not_responded_p, tbd_p = Stats.get_percent(source)
            self._labels[_index].config(text=source)
            self._labels[_index+1].config(text=f'Taotlusi {total_n} ({total_p}%)')
            self._labels[_index+2].config(text=f'Vastusega {responded_n} ({responded_p}%)')
            self._labels[_index+3].config(text=f'Vastuseta {not_responded_n} ({not_responded_p}%)')
            self._labels[_index+4].config(text=f'TBD {tbd_n} ({tbd_p}%)')
            _index += 5


class Tree(ttk.Treeview):
    
    _COLUMNS = {
        'id': 'ID',
        'date': 'Kuupäev',
        'title': 'Ametikoht',
        'company': 'Ettevõte',
        'status': 'Staatus'
    }
    
    
    def __init__(self, parent, name):
        ttk.Treeview.__init__(self, parent, height=31, columns=tuple(self._COLUMNS.keys()), show='headings', selectmode='browse')
        self.grid(row=0, column=0, sticky='nsew')
        self._parent = parent
        self.tab_name = name
        self._add_columns()
        self._load_data(name)
        self.bind('<<TreeviewSelect>>', self._edit_entry)
    
    
    def _add_columns(self):
        for key in self._COLUMNS:
            self.column(key, anchor=tk.CENTER)
            self.heading(key, text=self._COLUMNS[key])
    
    
    def _load_data(self, name: str) -> None:
        tab_data = Data.load_data(name)
        if (tab_data):
            for row in tab_data:
                row.insert(0, str(len(self.get_children())+1))
                self.insert('', tk.END, values=row)
    
    
    def add_new_entry(self, application_data: list[str]) -> None:
        application_data.insert(0, str(len(self.get_children())+1))
        self.insert('', tk.END, values=application_data)
    
    
    def _edit_entry(self, event):
        self._selected_entry = self.selection()[0]
        self._entry_record = self.item(self._selected_entry)['values']
        self._choose_status()
    
    
    def _choose_status(self):
        self._top = tk.Toplevel(self)
        self._top.geometry('400x100')
        self._top.title('Vali staatus')
        ttk.Label(self._top, text='Vali taotluse staatus').grid(row=0, column=0, columnspan=3, pady=10)
        ttk.Button(self._top, text='TBD', command=self._set_status_tbd).grid(row=1, column=0, padx=25, pady=10)
        ttk.Button(self._top, text='Eitav vastus', command=self._set_status_responded).grid(row=1, column=1, padx=25, pady=10)
        ttk.Button(self._top, text='Vastust pole', command=self._set_status_not_responded).grid(row=1, column=2, padx=25, pady=10)
    
    
    def _set_status_tbd(self):
        self._new_status = 'TBD'
        self._save_and_close()
    
    
    def _set_status_responded(self):
        self._new_status = 'Eitav vastus'
        self._save_and_close()
    
    
    def _set_status_not_responded(self):
        self._new_status = 'Vastust pole'
        self._save_and_close()
    
    
    def _save_and_close(self):
        if self._entry_record[-1] != self._new_status:
            Data.update_entry(self.tab_name, self._entry_record[0]-1, self._new_status)
            self._entry_record[-1] = self._new_status
            self.item(self._selected_entry, values=self._entry_record)
            self._parent.update_stats()
        self._top.destroy()
        self._top.update()


class Scroll(ttk.Scrollbar):
    
    def __init__(self, parent, obj, *args, **kwargs):
        ttk.Scrollbar.__init__(self, parent, orient='vertical', command=obj.yview, *args, **kwargs)
        self.grid(row=0, column=1, sticky='ns')


class DropdownMenu(ttk.OptionMenu):
    
    _dropdown_menus = {
        'source': ['CVKeskus', 'cv.ee', 'Töötukassa', 'E-kiri', 'Muu'],
        'day': [i for i in range(1, 32)],
        'month': ['Jaanuar', 'Veebruar', 'Märts', 'Aprill', 'Mai', 'Juuni', 'Juuli', 'August', 'September', 'Oktoober', 'November', 'Detsember'],
        'year': ['2024', '2025'],
        'status': ['TBD', 'Eitav vastus', 'Vastust pole']
    }
    _grid_indexes = {'source': 0, 'day': 1, 'month': 2, 'year': 3, 'status': 4}
    
    _paddings = {'source': 120, 'day': 5, 'month': 5, 'year': 5, 'status': 120}
    
    
    def __init__(self, parent, name):
        self._selected = tk.StringVar()
        self._selected.set(self._dropdown_menus[name][0])
        ttk.OptionMenu.__init__(self, parent, self._selected, self._dropdown_menus[name][0], *self._dropdown_menus[name])
        self.grid(row=0, column=self._grid_indexes[name], sticky='ew', **{'padx': self._paddings[name], 'pady': [10, 20]})
    
    
    def get_selected(self):
        return self._selected.get()


class InputField(ttk.Entry):
    
    _input_fields = {'title': 'Ametikoht', 'company': 'Ettevõte'}
    _indexes = {'title': [1, 0], 'company': [2, 0]}
    
    
    def __init__(self, parent, name):
        self._input_text = tk.StringVar(parent, self._input_fields[name])
        ttk.Entry.__init__(self, parent, textvariable=self._input_text, font=('Time New Roman', 13))
        self.grid(row=self._indexes[name][0], column=self._indexes[name][1], columnspan=5, sticky='nsew', **{'padx': 150, 'pady': [5, 0]})
    
    
    def get_text(self):
        return self._input_text.get()


class TextLabel(ttk.Label):
    
#     _grid_indexes = {
#         0:  [ 0, 0],  1: [ 1, 0],  2: [ 1, 1],  3: [ 1, 2],  4: [ 1, 3], # Kokku
#         5:  [ 2, 0],  6: [ 3, 0],  7: [ 3, 1],  8: [ 3, 2],  9: [ 3, 3], # CVKeskus
#         10: [ 4, 0], 11: [ 5, 0], 12: [ 5, 1], 13: [ 5, 2], 14: [ 5, 3], # cv.ee
#         15: [ 6, 0], 16: [ 7, 0], 17: [ 7, 1], 18: [ 7, 2], 19: [ 7, 3], # Tootukassa
#         20: [ 8, 0], 21: [ 9, 0], 22: [ 9, 1], 23: [ 9, 2], 24: [ 9, 3], # E-kiri
#         25: [10, 0], 26: [11, 0], 27: [11, 1], 28: [11, 2], 29: [11, 3] # Muu
#     }
    
    def __init__(self, parent, text, index):
        _font_size = 15 if index % 5 == 0 else 13
        ttk.Label.__init__(self, parent, text=text, font=('Times New Roman', _font_size))
        _row = index // 5 * 2
        _row += 0 if index % 5 == 0 else 1
        _column = index % 5 - 1 if index % 5 > 0 else 0
        _pady = [35, 5] if index % 5 == 0 else 5
        _columnspan = 4 if index % 5 == 0 else 1
        self.grid(row=_row, column=_column, columnspan=_columnspan, padx=[65, 40], pady=_pady)        


root = Root()
root.mainloop()
