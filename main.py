import pandas as pd
import PySimpleGUI as sg
import sequence_algorithms as seq
import result
from restrictions import restrictions
from messages import messages as msg

sg.theme("DarkBlue3")
sg.set_options(font=("Roboto", 12))

def get_nth_key(dictionary: dict, n=0) -> str:
    '''
    Script which takes a dictionary and outputs the key
    located in position n.
    '''
    if n < 0: n += len(dictionary)
    for i, key in enumerate(dictionary.keys()):
        if i == n: return key
    raise IndexError("dictionary index out of range")

def check_dna(dna: str) -> bool:
    '''
    Check if the user's input is a proper DNA sequence
    '''
    for char in dna:
        if char not in ['G', 'C', 'T', 'A']:
            sg.Popup(msg['bad_dna'])
            return False
    if len(dna) % 3 != 0:
        sg.Popup(msg['not_div_by_3'])
        return False
    return True

def update_rest(base: str, name: str, restrictions: dict) -> bool:
    '''
    Updates the restriction database. If user inputs
    empty string into name field, then it deletes the base
    from the database.
    '''
    for char in base:
        if char not in ['G', 'C', 'T', 'A']:
            sg.Popup(msg['bad_base'])
            return False
    if len(base) > 8 or len(base) < 4:
        sg.Popup(msg['bad_base_length'])
        return False
    if name == '':
        if base not in restrictions:
            sg.Popup(msg['base_not_found'], base)
            return False
        del restrictions[base]
    else: restrictions[base] = name
    return True

def main_window(saved_dna=''):
    '''

    '''
    dna, rest_bases, rest_names = '', [], []
    for key, value in restrictions.items():
        rest_bases.append(key)
        rest_names.append(value)
    headers = {'Base sequences (5\' 🠒 3\')' : rest_bases,
               'Restriction site name': rest_names}
    table = pd.DataFrame(headers)
    headings = list(headers)
    values = table.values.tolist()

    layout =  [[sg.T('DNA sequence'),sg.In(default_text=saved_dna, size=(30,1), key='dna'),
                sg.Button('Run'),
                sg.Button('Help')],
               [sg.Table(values=values,
                         headings=headings,
                         auto_size_columns=False,
                         display_row_numbers=True,
                         select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
                         enable_events=True,
                         key='-TABLE-',
                         col_widths=[20, 20])],
                [sg.T('Restr. base'),sg.In(default_text='', size=(10,1), key='rest_base'),
                 sg.T('Restr. name'),sg.In(default_text='', size=(10,1), key='rest_name'),
                 sg.Button('Add restriction', key='add_rest')],
                [sg.Button('Exit', button_color=('white', 'firebrick3'))]]

    window = sg.Window('iGEM',
                        text_justification='r',
                        default_element_size=(15,1)).Layout(layout)

    table = window['-TABLE-']
    user_click = True
    selected_indicies = []
    selected_items = []

    while True:
        event, values = window.Read()
        if event in ('Exit', None):
            break           # exit button clicked
        if event == 'Run' and check_dna(values['dna']):
            dna = values['dna']
            result.result_window(dna, selected_items)
        elif event == '-TABLE-':
            if user_click:
                if len(values['-TABLE-']) == 1:
                    select = values['-TABLE-'][0]
                    base = get_nth_key(restrictions, select)
                    item = (base, restrictions[base])
                    if select in selected_indicies:
                        selected_indicies.remove(select)
                        selected_items.remove(item)
                    else:
                        selected_indicies.append(select)
                        selected_items.append(item)
                    table.update(select_rows=selected_indicies)
                    user_click = False
                    print(selected_items)
            else:
                user_click = True

        elif event == 'add_rest':
            if update_rest(values['rest_base'],
                           values['rest_name'],
                           restrictions):
                window.close()
                main_window(saved_dna=dna)

if __name__ == '__main__':
    main_window()
