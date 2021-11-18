import PySimpleGUI as sg
import sequence_algorithms as seq

sg.theme("DarkBlue3")
sg.set_options(font=("Roboto", 12))

def result_window(dna: str, selected_items: list) -> None:
    '''
    Input: a DNA sequence, list indicating which restriction sites a user
    had choosed
    Output: the window containing the result information
    '''
    instances = seq.find_instances(dna, selected_items)
    positions = seq.find_positions(instances)
    result53 =  "In the forward strand (5'-3') of the DNA sequence there are " + \
                "following restriction sites.\n\n"
    result35 =  "In the reversed strand (3'-5') of the DNA sequence there are " + \
                "following restriction sites.\n\n"
    result_dna = seq.remove_instances(dna, instances)
    if not bool(positions):
        result53 = "There are no restriction sites in the forward strand of the given DNA."
        result35 = "There are no restriction sites in the reversed strand of the given DNA."
    for key, values in positions.items():
        values = ", ".join(map(str, values))
        result53 += key[0] + " named as " + \
                    key[1] + " found at positions " + \
                    values + ".\n\n"
        result35 += seq.complement(key[0]) + " named as " + \
                    key[1] + " found at positions " + \
                    values + ".\n\n"

    if len(selected_items) == 1:
        selected_restrictions = "The selected restriction site is " + \
                                str(selected_items[0][0]) + " — " + \
                                str(selected_items[0][1]) + "."
    elif len(selected_items) > 1:
        selected_restrictions = "The selected restriction sites are " + \
                                ", ".join([str(e[0]) + " — " + str(e[1]) \
                                for e in selected_items]) + "."
    else:
        selected_restrictions = "You haven't yet selected any restriction sites. " + \
                                "Please close this window, select the restrictions " + \
                                "you are interested in, and run the program."

    layout =  [[sg.Text("The forward strand of the DNA is:\n\n" + \
                        "and the reversed one is",
                        expand_y=True,
                        expand_x=True,
                        size=(35, None),
                        key="desription"),
                sg.Text(dna + '\n\n' + seq.complement(dna),
                        expand_y=True,
                        expand_x=True,
                        size=(40, None),
                        key="desription")],
               [sg.Text(selected_restrictions,
                       expand_y=True,
                       expand_x=True,
                       size=(80, None),
                       key="desription")],
               [sg.Multiline(result53,
                             background_color='#64778D',
                             text_color='white',
                             key='result53',
                             size=(37, 6),
                             disabled=True),
                sg.Multiline(result35,
                             background_color='#64778D',
                             text_color='white',
                             key='result35',
                             size=(37, 6),
                             disabled=True)],
                [sg.Text("The DNA sequences resulting after hiding the " + \
                         "selected restrictions:")],
                [sg.Multiline("(5\' - 3\'): " + result_dna + "\n\n(3\' - 5\'): " + \
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
