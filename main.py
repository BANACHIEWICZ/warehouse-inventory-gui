# PROGRAM MAIN
# =============

from data import przygotuj_dane
from gui import przygotuj_gui, uruchom_gui
from thread import uruchom_thread

def uruchom_program():
    print("1", flush=True)
    df_do_gui, lokacje_do_gui = przygotuj_dane()
    print("2", flush=True)
    przygotuj_gui(df_do_gui, lokacje_do_gui)
    print("3", flush=True)
    uruchom_thread()
    print("4", flush=True)
    uruchom_gui()
    print("5", flush=True)

uruchom_program()