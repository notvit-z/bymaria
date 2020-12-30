import pandas as pd
import matplotlib.pyplot as plt
import random


def show_prize_info(prizes_list, r):
    """
    Esta función agrega a la imagen la información del premio número "r" antes
    de que se realice el sorteo de éste. La información incluye el número del
    premio, la empresa que lo donó y el premio mismo.

    inputs:
        prizes_list -- pandas DaraFrame con la lista de premios, la que con-
                        tiene la información de la empresa y el premio que
                        donó.
        r -- índice de la iteración para indexar en la lista prizes_list.
    """
    # ploteando el número del premio
    plt.figtext(0.5, 0.47, f"Premio nº{r+1}", ha="center", size=35,
                fontname="Futura", weight="bold")

    plt.draw()
    plt.pause(1.5)

    # ploteando la empresa y el premio que donó
    plt.figtext(0.5, 0.4, "Por " + prizes_list["Empresa"].loc[r] + ":",
                ha="center", family="Futura", size=30, style="italic",
                bbox=dict(facecolor="none"))
    plt.figtext(0.5, 0.33, prizes_list["Premio"].loc[r], family="Futura",
                ha="center", fontsize=30)
    plt.draw()
    plt.pause(2.5)

    # ploteando frase-suspenso antes del sorteo
    plt.figtext(0.5, 0.26, "Y LA PERSONA GANADORA ES...", ha="center",
                family="Futura", weight="bold", size=30, color="red")

    plt.pause(3)


def show_winner(raffles_table, winning_number):
    """
    Esta función muestra en la imagen del sorteo la información del ganador del
    premio sorteado en ese momento. Esta información incluye su número de rifa
    y su nombre.

    inputs:
        raffles_table -- pandas DataFrame con la información de las rifas ven-
                        didas con sus respectivos compradores.
        winning_number -- número de rifa sorteado para el premio actual, el
                        cual se indexará en raffles_table para ver al ganador
    """
    plt.figtext(0.5, 0.2, "RIFA nº" + str(winning_number), ha="center",
                family="Futura", size=27, color=(0.929, 0.694, 0.125))
    plt.figtext(0.5, 0.11, raffles_table["Name"].iloc[winning_number-1],
                ha="center", family="Futura", size=58,
                color=(0.929, 0.694, 0.125))
    plt.pause(1)

    plt.figtext(0.5, 0.02, "FELICIDADES!", ha="center", family="Futura",
                size=40, color="red")
    plt.pause(4)


def append_winner_info(raffle_winners, prizes_list, raffles_table, winning_number, r):
    """
    Esta función agrega la información del ganador del premio "r" a una lista
    compilada de ganadores para que luego del sorteo puedan ser contactados.
    La información almacenada es el premio, la empresa donante, el número ga-
    nador, el nombre del ganador y su email.

    inputs:
        raffle_winners -- pandas DataFrame de la lista compilada de ganadores
                        a la cual se le va a agregar el ganador actual
        prizes_list -- pandas DataFrame con la lista de premios y las empre-
                        sas donantes.
        raffles_table -- pandas DataFrame de la lista de números de rifa con
                        la información de sus compradores.
        winning_number -- número de rifa ganadora del premio "r" sorteado.
        r -- índice del premio sorteado

    outputs:
        raffle_winners -- pandas DataFrame de la lista compilada de ganadores
                        una vez agregado el ganador del premio número "r"
    """
    winner_dict = {"Prize": [prizes_list["Premio"].iloc[r]],
                   "Prize Company": [prizes_list["Empresa"].iloc[r]],
                   "Winning Number": [winning_number],
                   "Winner Name": [raffles_table["Name"].iloc[winning_number-1]],
                   "Winner Email": [raffles_table["Email"].iloc[winning_number-1]]}

    winner_df = pd.DataFrame(data=winner_dict)

    raffle_winners = pd.concat([raffle_winners, winner_df], ignore_index=True)

    return raffle_winners


def hide_texts(fig):
    """
    Esta función esconde de la imagen los objetos de textos mostrando los
    premios y los ganadores, para que puedan ser renovados en la iteración
    del premio siguiente
    """
    for text in fig.texts:
        text.set_visible(False)


if __name__ == "__main__":
    mainpath = "/Users/vjtiznado/Dropbox/bymaria/files/"

    # importando la tabla de números de rifa
    # * si no existe este archivo, crear con raffles_table_from_orders_list.py
    raffles_table_filename = "raffles_table.csv"
    raffles_table = pd.read_csv(mainpath + raffles_table_filename)

    # importando la lista de premios
    column_names = ["Empresa", "Premio"]
    prizes_list = pd.read_csv(mainpath + "prize_list3.csv", usecols=[0, 1],
                              names=column_names)

    # importando imágenes del diseño del plot
    logo = plt.imread(mainpath + "logo3.jpg")
    afiche_izq = plt.imread(mainpath + "image1.jpeg")
    afiche_der = plt.imread(mainpath + "image2.jpeg")

    # creando la imagen basal para el sorteo con las tres imágenes anteriores
    fig, axs = plt.subplots(2, 3)
    [axi.set_axis_off() for axi in axs.ravel()]
    axs[0, 0].imshow(afiche_izq)
    axs[0, 1].imshow(logo)
    axs[0, 2].imshow(afiche_der)

    raffle_winners = pd.DataFrame()
    for r in range(0, len(prizes_list)):

        # mostrando el premio actual a sortear
        show_prize_info(prizes_list, r)

        # definiendo, de forma aleatoria, el número de rifa ganador del premio actual
        winning_number = random.randint(1, len(raffles_table))

        # mostrando al ganador del premio actual
        show_winner(raffles_table, winning_number)

        # agregando la información del ganador del premio actual
        # a la tabla compilada de ganadores
        raffle_winners = append_winner_info(raffle_winners, prizes_list,
                                            raffles_table, winning_number, r)

        # limpiando la imagen para el sorteo del próximo número
        hide_texts(fig)

        plt.pause(1)

    # guardando el archivo de la tabla compilada de ganadores
    raffle_winners.to_csv(mainpath + "raffles_winners.csv", index=False)
    plt.show(block=True)
