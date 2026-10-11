import tkinter as tk
from tkinter import ttk
from thread import kolejka_danych

okno = None

def przygotuj_gui(df_do_gui, lokacje_do_gui):
    global okno
    okno = tk.Tk()
    okno.title("Wizualizacja GUI")
    okno.geometry("800x500")

    pole_wyszukiwania = tk.Entry(
        okno,
        font=("Arial", 12),
    )
    pole_wyszukiwania.pack()

    def wyszukaj():
        tekst = pole_wyszukiwania.get()
        pasujace_lokacje = [
            lokacja for lokacja in lokacje_do_gui
            if tekst in lokacja
        ]
        for wiersz in tabela_lokacje.get_children():
            tabela_lokacje.delete(wiersz)
        for lokacja in pasujace_lokacje:
            tabela_lokacje.insert("", "end", values=(lokacja,))

    przycisk_szukaj = tk.Button(
        okno,
        text="Szukaj",
        command=wyszukaj
    )
    przycisk_szukaj.pack()

    def wyczysc():
        pole_wyszukiwania.delete(0, tk.END)
        wyszukaj()

    przycisk_wyczysc = tk.Button(
        okno,
        text="Wyczyść",
        command=wyczysc
    )
    przycisk_wyczysc.pack()

    ramka_dla_tabeli = tk.Frame(okno, borderwidth=1, relief="solid")
    ramka_dla_tabeli.pack()

    kolumny_lokacje = ("Lokacja",)
    tabela_lokacje = ttk.Treeview(
        ramka_dla_tabeli, columns=kolumny_lokacje, show="headings",
    )
    for kolumna_lokacje in kolumny_lokacje:
        tabela_lokacje.heading(kolumna_lokacje, text=kolumna_lokacje, anchor="center")
    tabela_lokacje.column("Lokacja", width=90, anchor="center")
    for wiersz_lokacji in lokacje_do_gui:
        tabela_lokacje.insert("", "end", values=(wiersz_lokacji,))
    tabela_lokacje.pack(
        side=tk.LEFT
    )

    tabela_lokacje_scroll = ttk.Scrollbar(
        ramka_dla_tabeli,
        command=tabela_lokacje.yview,
    )
    tabela_lokacje_scroll.pack(
        side=tk.RIGHT,
        fill=tk.Y
    )
    tabela_lokacje.configure(yscrollcommand=tabela_lokacje_scroll.set)

    def pokaz_szczegoly(okno, wybrana_lokacja):
        dane_lokacji = df_do_gui[
            df_do_gui["Lokacja"] == wybrana_lokacja
            ]

        # print("POKAZUJE SZCZEGOLY", flush=True)
        # print(dane_lokacji, flush=True)
        szczegoly_nowe_okno = tk.Toplevel(okno)
        szczegoly_nowe_okno.title("Szczegóły lokacji")
        szczegoly_nowe_okno.geometry("700x300")

        kolumny_szczegoly_lokacji = dane_lokacji.columns.tolist()
        tabela_szczegoly_lokacji = ttk.Treeview(
            szczegoly_nowe_okno,
            columns=kolumny_szczegoly_lokacji,
            show="headings"
        )

        for kolumna_szczegoly_lokacji in kolumny_szczegoly_lokacji:
            tabela_szczegoly_lokacji.heading(
                kolumna_szczegoly_lokacji,
                text=kolumna_szczegoly_lokacji,
            )
        tabela_szczegoly_lokacji.column("Towar", width=70, anchor="center")
        tabela_szczegoly_lokacji.column("Ilość", width=160, anchor="center")
        tabela_szczegoly_lokacji.column("Lokacja", width=70, anchor="center")
        tabela_szczegoly_lokacji.column("Exp", width=80, anchor="center")
        tabela_szczegoly_lokacji.column("Referencja", width=80, anchor="center")
        tabela_szczegoly_lokacji.column("Opis towaru", width=80, anchor="center")
        tabela_szczegoly_lokacji.column("Pal", width=80, anchor="center")

        # print("WIERSZE DO TABELI:", flush=True)
        # print(dane_lokacji.values.tolist(), flush=True)

        wiersze = dane_lokacji.values.tolist()
        for wiersz in wiersze:
            tabela_szczegoly_lokacji.insert("", "end", values=wiersz)

        tabela_szczegoly_lokacji.pack()

        def odswiez_szczegoly():
            # print("Odświeżam szczegóły:", wybrana_lokacja, flush=True)
            for wiersz in tabela_szczegoly_lokacji.get_children():
                tabela_szczegoly_lokacji.delete(wiersz)

            nowe_dane_lokacji = df_do_gui[
                df_do_gui["Lokacja"] == wybrana_lokacja
                ]

            wiersze = nowe_dane_lokacji.values.tolist()

            for wiersz in wiersze:
                tabela_szczegoly_lokacji.insert(
                    "",
                    "end",
                    values=wiersz
                )

            szczegoly_nowe_okno.after(1000, odswiez_szczegoly)
        odswiez_szczegoly()

    def klikniecie_lokacji(event):
        # id_wybranego_wiersza = tabela_lokacje.selection()
        id_wybranego_wiersza = tabela_lokacje.identify_row(event.y)

        if not id_wybranego_wiersza:
            return

        dane_wiersza_lokacji = tabela_lokacje.item(id_wybranego_wiersza)
        # dane_wiersza_lokacji = tabela_lokacje.item(id_wybranego_wiersza[0])
        wybrana_lokacja = dane_wiersza_lokacji.get("values")[0]
        # print(df_do_gui, flush=True)
        # print("DF PRZY KLIKNIĘCIU:", flush=True)
        # print(df_do_gui, flush=True)
        # print("WYBRANA LOKACJA:", wybrana_lokacja, flush=True)
        dane_lokacji = df_do_gui[df_do_gui["Lokacja"] == wybrana_lokacja]

        # print("DANE LOKACJI:", flush=True)
        # print(dane_lokacji, flush=True)

        pokaz_szczegoly(okno, wybrana_lokacja)

    tabela_lokacje.bind("<Double-Button-1>", klikniecie_lokacji)

    def sprawdz_nowe_dane():
        nonlocal df_do_gui, lokacje_do_gui
        if not kolejka_danych.empty():
            nowe_df_do_gui, nowe_lokacje_do_gui = kolejka_danych.get()
            # print("GUI DF:", type(nowe_df_do_gui), flush=True)
            # print("GUI LOKACJE:", type(nowe_lokacje_do_gui), flush=True)
            # print("Gui odebralo nowe dane", flush=True)
            # print(nowe_df_do_gui, flush=True)
            # print(type(nowe_df_do_gui), flush=True)
            # print(type(nowe_lokacje_do_gui), flush=True)
            df_do_gui = nowe_df_do_gui

            lokacje_do_gui = nowe_lokacje_do_gui

            for wiersz in tabela_lokacje.get_children():
                tabela_lokacje.delete(wiersz)

            for lokacja in nowe_lokacje_do_gui:
                tabela_lokacje.insert(
                    "",
                    "end",
                    values=(lokacja,)
                )

        okno.after(1000, sprawdz_nowe_dane)
    sprawdz_nowe_dane()
    # okno.mainloop()
def uruchom_gui():
    okno.mainloop()
# przygotuj_gui()