import pandas as pd
import numpy as np


def fill_empty_billing_names(df):
    """
    Esta función soluciona que hayan "Billing Names" no asignados (celda vacía)
    en algunas posiciones de la lista de órdenes, lo cual ocurría cuando los
    clientes hacían órdenes de compra consecutivas. La función, en cada celda
    vacía, incluye el Billing Name de la celda anterior.

    inputs:
        df -- DataFrame de pandas con las órdenes de compra de los clientes.

    outputs:
        df -- DataFrame de pandas con las órdenes de compra de los
                    clientes, pero habiendo rellenado los Billing Name que es-
                    taban vacíos
    """
    nans_loc = np.flatnonzero(pd.isna(df["Billing Name"]))
    for nans in nans_loc:
        df["Billing Name"].iloc[nans] = df["Billing Name"].iloc[nans-1]

    return df


def create_single_client_table(df, idx):
    """
    Esta función toma la información del cliente de una determinada orden de
    compra de rifa y crea una lista donde su información se repite tantas veces
    como rifas compró. La función está pensada para correr iterativamente en
    la función create_raffles_table().

    inputs:
        df -- pandas DataFrame con la tabla de órdenes de compra de rifas de
                todos los clientes.
        idx -- índice de la tabla de órdenes de compra con el cual se extraerá
                la información del cliente.

    outputs:
        single_client_df -- pandas DataFrame con la información del cliente de
                            la compra 'idx', repetida tantas veces como rifas
                            compró.
    """
    raffles_buyed = df["Lineitem quantity"].iloc[idx]

    single_client_dict = {"Order Number": [df["Name"].iloc[idx]]*raffles_buyed,
                          "Name": [df["Billing Name"].iloc[idx]]*raffles_buyed,
                          "Email": [df["Email"].iloc[idx]]*raffles_buyed}

    single_client_df = pd.DataFrame(data=single_client_dict)

    return single_client_df


def create_raffles_table(raffle_orders):
    """
    Esta función toma la lista de órdenes de compra de rifas y construye una
    lista de números de rifa, a los cuales se les asigna la información de cada
    cliente para contactarlo después del sorteo. La función toma la información
    de cada cliente y, basándose en cuántas rifas compró, repite su información
    en la nueva lista para que finalmente se le asignen tantos números como
    rifas compró.

    inputs:
        raffle_orders -- pandas DataFrame con las órdenes de compra de rifas.

    outputs:
        raffles_table -- tabla de números de rifa con la información de cada
                        cliente para contactarlo después del sorteo.
    """
    raffles_table = pd.DataFrame()
    for i in range(len(raffle_orders)):
        single_client_table = create_single_client_table(raffle_orders, i)
        raffles_table = pd.concat([raffles_table, single_client_table],
                                  ignore_index=True)

    raffles_table["num_rifa"] = np.arange(1, len(raffles_table)+1)

    return raffles_table


if __name__ == "__main__":
    # importando archivo .csv con las órdenes de compra de internet
    mainpath = "/Users/vjtiznado/Dropbox/bymaria/files/"
    orders_filename = "PEDIDOS_RIFA.csv"
    columns_to_use = ["Name", "Billing Name", "Email", "Lineitem quantity",
                      "Lineitem name"]
    orders_all = pd.read_csv(mainpath + orders_filename,
                             usecols=columns_to_use)

    orders_all = fill_empty_billing_names(orders_all)

    # filtrar la tabla de órdenes y considerar sólo las compras de rifas
    raffle_bool = orders_all["Lineitem name"].str.contains("RIFA")
    raffle_orders = orders_all[raffle_bool]

    # creando una lista de números de rifa
    # la lista considera cuántas rifas compró cada cliente
    raffles_table = create_raffles_table(raffle_orders)

    # guardando la lista de números de rifa como archivo csv
    raffles_table.to_csv(mainpath + "raffles_table.csv", index=False)
