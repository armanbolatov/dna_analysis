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
    result_dna = seq.remove_instances(dna, instances)

    result53 = ("In the forward strand (5'-3') of the DNA sequence there are "
                "following restriction sites:\n\n") if bool(positions) else \
               ("There are no restriction sites in the "
                "forward strand of the given DNA.")
    result35 = ("In the reversed strand (3'-5') of the DNA sequence there are "
                "following restriction sites:\n\n") if bool(positions) else \
               ("There are no restriction sites in the "
                "reversed strand of the given DNA.")

    for key, values in positions.items():
        values = ", ".join(map(str, values))
        result53 += (f"{key[0]} named as {key[1]} found at "
                     f"{'positions' if len(values) > 1 else 'position'} "
                     f"{values}.\n\n")
        result35 += (f"{seq.complement(key[0])} named as {key[1]} found at "
                     f"{'positions' if len(values) > 1 else 'position'} "
                     f"{values}.\n\n")

    if len(selected_items) == 1:
        selected_rests = (f"The selected restriction site is "
                          f"{selected_items[0][0]} — {selected_items[0][1]}.")
    elif len(selected_items) > 1:
        rests = ", ".join([f"{e[0]} — {e[1]}" for e in selected_items])
        selected_rests = f"The selected restriction sites are {rests}."
    else:
        selected_rests = ("You haven't yet selected any restriction sites. "
                          "Please close this window, select the restrictions "
                          "you are interested in, and run the program.")

    layout =  [[sg.Text(("The forward strand of the DNA is:\n\n"
                         "and the reversed one is"),
                        expand_y=True, expand_x=True,
                        size=(35, None), key="desription"),
                sg.Text(dna + '\n\n' + seq.complement(dna),
                        expand_y=True, expand_x=True,
                        size=(40, None), key="desription")],
               [sg.Text(selected_rests,
                        expand_y=True, expand_x=True,
                        size=(80, None), key="desription")],
               [sg.Multiline(result53, background_color='#64778D',
                             text_color='white', key='result53',
                             size=(37, 6), disabled=True),
                sg.Multiline(result35, background_color='#64778D',
                             text_color='white', key='result35',
                             size=(37, 6), disabled=True)],
                [sg.Text(("The DNA sequences resulting after hiding the "
                          "selected restrictions:"))],
                [sg.Multiline((f"(5\' - 3\'): {result_dna} \n\n(3\' - 5\'): "
                               f"{seq.complement(result_dna)}"),
                              background_color='#64778D', text_color='white',
                              key='result_dna', size=(78, 4), disabled=True)]]

    window = sg.Window("Resulting DNA", modal=True).Layout(layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    window.close()
