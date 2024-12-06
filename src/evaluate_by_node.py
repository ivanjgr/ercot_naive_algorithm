import pandas as pd
from os.path import join
from tqdm import tqdm
from strategy import Strategy, get_node_data, TimeBasedRule
from results import Results


def evaluate_performance(df_node: pd.DataFrame, strategy: Strategy) -> pd.DataFrame:
    df_node_local = df_node.copy()
    df_node_local["bid_price"] = df_node_local.index.map(strategy.apply_rules)
    df_node_local["awarded"] = (df_node_local["bid_price"] >= df_node_local["SPP_DA"]).astype(int)
    df_node_local["profit"] = (df_node_local["SPP_RT"] - df_node_local["SPP_DA"]) * df_node_local["awarded"]
    df_node_local["rules"] = ' & '.join([str(rule) for rule in strategy.rules])
    df_node_local["bid_price"] = df_node_local.apply(lambda x: x["SPP_DA"] + 1 if x["awarded"] == 1 else x["SPP_DA"] - 1, axis=1)
    r = Results(df_node_local)
    print(r)
    r.save_results()
    r.generate_plot()

def evaluate_nebula():
    # Load the virtual trading data
    node_data = get_node_data("NEBULA_RN")
    # Define the strategy
    rules = [
        TimeBasedRule(day_of_week='Tuesday', hour_range=list(range(4, 10)) + list(range(19, 24))),
        TimeBasedRule(day_of_week='Wednesday', hour_range=list(range(5, 9))),
    ]
    strategy = Strategy("NEBULA_RN", rules)
    # Evaluate the strategy
    results = evaluate_performance(node_data, strategy)

    # To save replace -inf with -999
    #results = results.replace(-float('inf'), -999)
    #results = results.replace(float('inf'), 999)
    # Where awarded = 1, bid_price = SPP_DA + 1, otherwise bid_price = SPP_DA - 1
    results["bid_price"] = results.apply(lambda x: x["SPP_DA"] + 1 if x["awarded"] == 1 else x["SPP_DA"] - 1, axis=1)
    results.to_csv("../results/nodo_NEBULA_RN.csv")


def evaluate_massengl():
    # Load the virtual trading data
    node_data = get_node_data("MASSENGL_G8")
    # Define the strategy
    rules = [
        TimeBasedRule(day_of_week='Monday', hour_range=[7, 20, 21, 22, 23]),
        TimeBasedRule(day_of_week='Tuesday', hour_range=[0, 1, 2, 3, 4, 5, 6, 21]),
        TimeBasedRule(day_of_week='Wednesday', hour_range=[7, 22, 23] ),
        TimeBasedRule(day_of_week='Thursday', hour_range=[0, 1, 2, 3, 4, 5, 6, 7, 8] ),
        TimeBasedRule(day_of_week='Friday', hour_range=[1, 2, 3, 20, 21, 22, 23] ),
        TimeBasedRule(day_of_week='Saturday', hour_range=[1, 2, 3, 4, 5, 6, 19] ),
        TimeBasedRule(day_of_week='Sunday', hour_range=[1, 2, 3, 4, 5, 6, 7, 22, 23] ),
    ]
    strategy = Strategy("MASSENGL_G8", rules)
    # Evaluate the strategy
    evaluate_performance(node_data, strategy)


def evaluate_aeec():
    # Load the virtual trading data
    node_data = get_node_data("AEEC")
    # Define the strategy
    rules = [
        TimeBasedRule(day_of_week='Monday', hour_range=[20, 21, 22, 23]),
        TimeBasedRule(day_of_week='Tuesday', hour_range=[20]),
        TimeBasedRule(day_of_week='Wednesday', hour_range=[23]),
        TimeBasedRule(day_of_week='Thursday', hour_range=[1, 2, 5, 6, 21, 23]),
        TimeBasedRule(day_of_week='Friday', hour_range=[1, 2, 21, 22, 23]),
        TimeBasedRule(day_of_week='Saturday', hour_range=[6]),
        TimeBasedRule(day_of_week='Sunday', hour_range=[1, 4]),
    ]
    strategy = Strategy("AEEC", rules)
    # Evaluate the strategy
    results = evaluate_performance(node_data, strategy)
    # To save replace -inf with -999
    #results = results.replace(-float('inf'), -999)
    #results = results.replace(float('inf'), 999)
    # Where awarded = 1, bid_price = SPP_DA + 1, otherwise bid_price = SPP_DA - 1
    results["bid_price"] = results.apply(lambda x: x["SPP_DA"] + 1 if x["awarded"] == 1 else x["SPP_DA"] - 1, axis=1)


def evaluate_pale_ess():
    # Load the virtual trading data
    node_data = get_node_data("PALE_ESS_EN")
    # Define the strategy
    rules = [
        TimeBasedRule(day_of_week='Monday', hour_range=[20, 21, 22, 23]),
        TimeBasedRule(day_of_week='Tuesday', hour_range=[20]),
        TimeBasedRule(day_of_week='Wednesday', hour_range=[23]),
        TimeBasedRule(day_of_week='Thursday', hour_range=[1, 2, 5, 6, 21, 23]),
        TimeBasedRule(day_of_week='Friday', hour_range=[1, 2, 21, 22, 23]),
        TimeBasedRule(day_of_week='Sunday', hour_range=[1]),
    ]
    strategy = Strategy("PALE_ESS_EN", rules)
    # Evaluate the strategy
    evaluate_performance(node_data, strategy)


def evaluate_astra_rn():
    # Load the virtual trading data
    node_data = get_node_data("ASTRA_RN")
    # Define the strategy
    rules = [
        TimeBasedRule(day_of_week='Monday', hour_range=[21, 22, 23]),
        TimeBasedRule(day_of_week='Tuesday', hour_range=[0, 1, 2, 3, 4, 5, 6, 21]),
        TimeBasedRule(day_of_week='Wednesday', hour_range=[3, 23]),
        TimeBasedRule(day_of_week='Thursday', hour_range=[1, 2, 3, 4, 5, 6, 7, 23]),
        TimeBasedRule(day_of_week='Friday', hour_range=[1, 2, 3, 21, 22, 23]),
        TimeBasedRule(day_of_week='Saturday', hour_range=[1, 6, 7]),
        TimeBasedRule(day_of_week='Sunday', hour_range=[0, 1, 2, 3, 4, 5, 6, 7]),
    ]
    strategy = Strategy("ASTRA_RN", rules)
    # Evaluate the strategy
    evaluate_performance(node_data, strategy)


def evaluate_hrfwind_all():
    # Load the virtual trading data
    node_data = get_node_data("HRFDWIND_ALL")
    # Define the strategy
    rules = [
        TimeBasedRule(day_of_week='Monday', hour_range=[21, 22, 23]),
        TimeBasedRule(day_of_week='Tuesday', hour_range=[0, 1, 2, 3, 4, 5, 6, 21]),
        TimeBasedRule(day_of_week='Wednesday', hour_range=[3, 23]),
        TimeBasedRule(day_of_week='Thursday', hour_range=[1, 2, 3, 4, 5, 6, 7, 23]),
        TimeBasedRule(day_of_week='Friday', hour_range=[1, 2, 3, 21, 22, 23]),
        TimeBasedRule(day_of_week='Saturday', hour_range=[1, 6, 7]),
        TimeBasedRule(day_of_week='Sunday', hour_range=[0, 1, 2, 3, 4, 5, 6, 7])
    ]
    strategy = Strategy("HRFDWIND_ALL", rules)
    # Evaluate the strategy
    evaluate_performance(node_data, strategy)


def evaluate_mariah_all():
    # Load the virtual trading data
    node_data = get_node_data("MARIAH_ALL")
    # Define the strategy
    rules = [
        TimeBasedRule(day_of_week='Monday', hour_range=[21, 22, 23]),
        TimeBasedRule(day_of_week='Tuesday', hour_range=[0, 1, 2, 3, 4, 5, 6, 21]),
        TimeBasedRule(day_of_week='Wednesday', hour_range=[3, 23]),
        TimeBasedRule(day_of_week='Thursday', hour_range=[1, 2, 3, 4, 5, 6, 7, 23]),
        TimeBasedRule(day_of_week='Friday', hour_range=[1, 2, 3, 21, 22, 23]),
        TimeBasedRule(day_of_week='Saturday', hour_range=[1, 6, 7]),
        TimeBasedRule(day_of_week='Sunday', hour_range=[0, 1, 2, 3, 4, 5, 6, 7])
    ]
    strategy = Strategy("MARIAH_ALL", rules)
    # Evaluate the strategy
    evaluate_performance(node_data, strategy)


def evaluate_sspurtwind_all():
    # Load the virtual trading data
    node_data = get_node_data("SSPURT_WIND1")
    # Define the strategy
    rules = [
        TimeBasedRule(day_of_week='Monday', hour_range=[21, 22, 23]),
        TimeBasedRule(day_of_week='Tuesday', hour_range=[1, 2, 3, 4, 5, 6]),
        TimeBasedRule(day_of_week='Wednesday', hour_range=[3, 23]),
        TimeBasedRule(day_of_week='Thursday', hour_range=[1, 2, 3, 4, 6, 7, 23]),
        TimeBasedRule(day_of_week='Friday', hour_range=[1, 2, 3, 21, 22, 23]),
        TimeBasedRule(day_of_week='Saturday', hour_range=[6, 7]),
        TimeBasedRule(day_of_week='Sunday', hour_range=[0, 1, 2, 3, 4, 5, 6, 7])
    ]
    strategy = Strategy("SSPURT_WIND1", rules)
    # Evaluate the strategy
    evaluate_performance(node_data, strategy)


def evaluate_fryeslr_all():
    # Load the virtual trading data
    node_data = get_node_data("FRYE_SLR_ALL")
    # Define the strategy
    rules = [
        TimeBasedRule(day_of_week='Monday', hour_range=[21, 22, 23]),
        TimeBasedRule(day_of_week='Tuesday', hour_range=[1, 2, 3, 4, 5, 6]),
        TimeBasedRule(day_of_week='Wednesday', hour_range=[23]),
        TimeBasedRule(day_of_week='Thursday', hour_range=[1, 2, 3, 4, 6, 7]),
        TimeBasedRule(day_of_week='Friday', hour_range=[1, 2, 3, 21, 22, 23]),
        TimeBasedRule(day_of_week='Saturday', hour_range=[6, 7]),
        TimeBasedRule(day_of_week='Sunday', hour_range=[0, 1, 2, 3, 4, 5, 6, 7])
    ]
    strategy = Strategy("FRYE_SLR_ALL", rules)
    # Evaluate the strategy
    evaluate_performance(node_data, strategy)


def evaluate_dce():
    # Load the virtual trading data
    node_data = get_node_data("DC_E")
    # Define the strategy
    rules = [
        TimeBasedRule(day_of_week='Monday', hour_range=[6, 14]),
        TimeBasedRule(day_of_week='Tuesday', hour_range=[1, 2, 3, 4, 5]),
        TimeBasedRule(day_of_week='Thursday', hour_range=[6]),
        TimeBasedRule(day_of_week='Saturday', hour_range=[1, 2]),
        TimeBasedRule(day_of_week='Sunday', hour_range=[1, 3, 4, 23])
    ]
    strategy = Strategy("DC_E", rules)
    # Evaluate the strategy
    evaluate_performance(node_data, strategy)


def evaluate_dcl():
    # Load the virtual trading data
    node_data = get_node_data("DC_L")
    # Define the strategy
    rules = [
        TimeBasedRule(day_of_week='Tuesday', hour_range=[23]),
        TimeBasedRule(day_of_week='Wednesday', hour_range=[4, 5]),
        TimeBasedRule(day_of_week='Thursday', hour_range=[22, 23]),
        TimeBasedRule(day_of_week='Friday', hour_range=[1, 2, 23]),
        TimeBasedRule(day_of_week='Saturday', hour_range=[20, 21, 22, 23]),
        TimeBasedRule(day_of_week='Sunday', hour_range=[18]),
    ]
    strategy = Strategy("DC_L", rules)
    # Evaluate the strategy
    evaluate_performance(node_data, strategy)


def evaluate_lz_north():
    # Load the virtual trading data
    node_data = get_node_data("LZ_NORTH")
    # Define the strategy
    rules = [
        TimeBasedRule(day_of_week='Monday', hour_range=[6, 14]),
        TimeBasedRule(day_of_week='Tuesday', hour_range=[1, 2, 3, 4]),
        TimeBasedRule(day_of_week='Thursday', hour_range=[6]),
        TimeBasedRule(day_of_week='Saturday', hour_range=[1, 2, 3, 23]),
        TimeBasedRule(day_of_week='Sunday', hour_range=[3, 4, 23]),
    ]
    strategy = Strategy("LZ_NORTH", rules)
    # Evaluate the strategy
    evaluate_performance(node_data, strategy)


def evaluate_all_nodes():
    data_base_path = '../data/'
    complete_df_sorted = pd.read_csv(join(data_base_path, 'virtual_trading_weekday_hour.csv'))
    node_list = complete_df_sorted['settlementPoint_'].unique()

    cond = lambda x: x > 1
    for node in tqdm(node_list):
        test_node_data = complete_df_sorted[complete_df_sorted['settlementPoint_'] == node].copy()

        df_node_weekly = test_node_data.sort_values(by=["day_of_week_", "hour_"])
        rules = []
        for dow in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            h_list = []
            for hour in range(24):
                df_local = df_node_weekly[(df_node_weekly["day_of_week_"] == dow) & (df_node_weekly["hour_"] == hour)]
                if cond(df_local["return_DA_RT_median"].values[0]):
                    h_list.append(hour)

            if len(h_list) > 0:
                rules.append(TimeBasedRule(day_of_week=dow, hour_range=h_list))

        strategy = Strategy(node, rules)
        evaluate_performance(get_node_data(node), strategy)

if __name__ == "__main__":
    evaluate_all_nodes()