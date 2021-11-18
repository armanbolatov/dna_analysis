import PySimpleGUI as sg

sg.theme("DarkBlue3")
sg.set_options(font=("Roboto", 12))

with open('help_text.txt', 'r') as f:
    text = f.read()

def help_window() -> None:
    layout =  [[sg.Text(text, size=(60, None))]]
    window = sg.Window("Help", size=(None, None), modal=True).Layout(layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    window.close()
