import pandas as pd

def przygotuj_dane():
    df = pd.read_excel(
        "przykładowe_dane.xlsx",
        sheet_name="Arkusz1",
        usecols=["Towar", "Lokacja", "Ilość", "Referencja", "Exp", "Pal", "Opis towaru"],
        dtype={"Lokacja": str}
    )

    df_do_gui = df.sort_values(by=["Lokacja", "Towar"], ascending=True)
    df_do_gui = df_do_gui.fillna("")

    lokacje_do_gui = df_do_gui["Lokacja"].unique().tolist()

    # print(df["Lokacja"].tolist())
    # print(df_do_gui["Lokacja"].tolist())
    # print(df)
    # print(df_do_gui)
    # print(lokacje_do_gui)
    return df_do_gui, lokacje_do_gui
