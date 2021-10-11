import pandas as pd
import PySimpleGUI as sg
import sequence_algorithms as seq
from restrictions import restrictions
from messages import messages as msg

sg.theme("DarkBlue3")
sg.set_options(font=("Roboto", 12))

def result_window(dna: str, selected_items: list) -> None:

    instances = seq.find_instances(dna, selected_items)
    positions = seq.find_positions(instances)
    result53 = "In the 5'-3' DNA sequence there are following restrictions.\n\n"
    result35 = "In the 3'-5' DNA sequence there are following restrictions.\n\n"
    result_dna = seq.remove_instances(dna, instances)
    print(positions)
    if not bool(positions):
        result53 = "There are no restriction sites in the 3'-5' of the given DNA."
        result35 = "There are no restriction sites in the 3'-5' of the given DNA."
    for key, values in positions.items():
        values = ", ".join(map(str, values))
        result53 += key[0] + " named as " + \
                    key[1] + " found at positions " + \
                    values + ".\n\n"
        result35 += seq.complement(key[0]) + " named as " + \
                    key[1] + " found at positions " + \
                    values + ".\n\n"

    if len(selected_items) != 0:
        selected_restrictions = "The selected restriction sites are " + \
                                ", ".join([str(e[0]) + " — " + str(e[1]) \
                                for e in selected_items]) + "."
    else:
        selected_restrictions = "You haven't yet selected any restriction sites. " + \
                                "Please close this window, select the restrictions " + \
                                "you are interested in, and run the program."

    layout =  [[sg.Text("The given DNA sequence in 5'-3' is " + \
                        dna + " and in 3'-5' is " + seq.complement(dna) + \
                        "\n\n" + selected_restrictions,
                        expand_y=True,
                        expand_x=True,
                        size=(80, None),
                        key="desription")],
               [sg.Multiline(result35,
                             background_color='#64778D',
                             text_color='white',
                             key='result35',
                             size=(37, 6),
                             disabled=True),
                sg.Multiline(result53,
                             background_color='#64778D',
                             text_color='white',
                             key='result53',
                             size=(37, 6),
                             disabled=True)],
                [sg.Text("After deleting the")],
                [sg.Multiline("(5\' 🠒 3\'): " + result_dna + "\n\n(3\' 🠒 5\'): " + \
                              seq.complement(result_dna),
                              background_color='#64778D',
                              text_color='white',
                              key='result_dna',
                              size=(78, 4),
                              disabled=True)]]
    window = sg.Window("Resulting DNA", size=(None, None), modal=True).Layout(layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    window.close()
