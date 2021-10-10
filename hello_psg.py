import pandas as pd
import PySimpleGUI as sg
import restrictions as rst
from messages import messages as msg
from sequence_analysis import find_instances

sg.theme("DarkBlue3")
sg.set_options(font=("Roboto", 10))

restrictions = {
    'GAATC': 'EcoRI',
    'TCTAGA': 'XbaI',
    'ACTAGT': 'SpeI',
    'CTGCAG': 'PstI',
    'GCGGCCGC': 'NotI',
    'GCTCTCC': 'SapI',
    'GGTCTC': 'BcaI'
}

def get_nth_key(dictionary: dict, n=0) -> str:
    '''
    Script which takes a dictionary and outputs a
    '''
    if n < 0: n += len(dictionary)
    for i, key in enumerate(dictionary.keys()):
        if i == n: return key
    raise IndexError("dictionary index out of range")

def update_rest(base: str, name: str, restrictions: dict) -> bool:
    '''
    Input:
    '''
    for char in base:
        if char not in ['G', 'C', 'T', 'A']:
            sg.Popup(msg['bad_base'])
            return False
    if name == '':
        if base not in restrictions:
            sg.Popup(msg['base_not_found'], base)
            return False
        del restrictions[base]
    else:
        restrictions[base] = name
    return True

def result_window(dna: str, result: str) -> None:
    layout =  [[sg.Text("New Window", key="new")],
               [sg.Text(result, font=('Courier', 12), key='result')]]
    window = sg.Window("Resulting DNA", size=(300, 200), modal=True).Layout(layout)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

    window.close()

def main_window(saved_dna=''):
    '''

    '''
    rest_bases, rest_names = [], []
    for key, value in restrictions.items():
        rest_bases.append(key)
        rest_names.append(value)
    headers = { 'Base sequences (5\' -> 3\')' : rest_bases,
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
                [sg.T('Rest name'),sg.In(default_text='', size=(10,1), key='rest_base'),
                 sg.T('Rest seq'),sg.In(default_text='', size=(10,1), key='rest_name'),
                 sg.Button('Add restriction', key='add_rest')],
                [sg.Button('Add multiple restrictions', key='add_multiple_rests'),
                 sg.Button('Exit', button_color=('white', 'firebrick3'))]]

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
        if event == 'Run':
            dna = values['dna']
            result = find_instances(dna, selected_items)
            print(len(dna), result)
            result_window(dna, result)
        elif event == '-TABLE-':
            if user_click:
                if len(values['-TABLE-']) == 1:
                    select = values['-TABLE-'][0]
                    if select in selected_indicies:
                        selected_indicies.remove(select)
                        base_name = get_nth_key(restrictions, select)
                        item = (base_name, restrictions[base_name])
                        selected_items.remove(item)
                    else:
                        selected_indicies.append(select)
                        base_name = get_nth_key(restrictions, select)
                        item = (base_name, restrictions[base_name])
                        selected_items.append(item)
                    table.update(select_rows=selected_indicies)
                    user_click = False
                    print(selected_items)
            else:
                user_click = True

        elif event == 'add_rest':
            if update_rest( values['rest_base'],
                            values['rest_name'],
                            restrictions):
                window.close()
                main_window(saved_dna=dna)

main_window()
