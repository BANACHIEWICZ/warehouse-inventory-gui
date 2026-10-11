import threading
import time

from data import przygotuj_dane
from queue import Queue
kolejka_danych = Queue()

def automatyczne_odswiezanie():
    # print("Thread start", flush=True)
    while True:
        nowe_df_do_gui, nowe_lokacje_do_gui = przygotuj_dane()
        # print("Pobrano nowe dane", flush=True)
        # print("DF:", type(nowe_df_do_gui), flush=True)
        # print("LOKACJE:", type(nowe_lokacje_do_gui), flush=True)
        kolejka_danych.put(
            (nowe_df_do_gui, nowe_lokacje_do_gui)
        )
        time.sleep(10)
        # print("Odświeżam", flush=True)
        # print(nowe_df_do_gui, flush=True)

def uruchom_thread():
    # print("Uruchamiam thread", flush=True)
    thread = threading.Thread(
        target=automatyczne_odswiezanie,
        daemon=True
    )
    thread.start()
    # print("Thread uruchomiony", flush=True)

