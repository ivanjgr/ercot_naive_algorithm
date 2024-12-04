import pandas as pd
from strategy import Strategy, get_node_data, TimeBasedRule
from results import Results


def evaluate_performance(df_node: pd.DataFrame, strategy: Strategy) -> pd.DataFrame:
    df_node_local = df_node.copy()
    df_node_local["bid_price"] = df_node_local.index.map(strategy.apply_rules)
    df_node_local["awarded"] = (df_node_local["bid_price"] >= df_node_local["SPP_DA"]).astype(int)
    df_node_local["profit"] = (df_node_local["SPP_RT"] - df_node_local["SPP_DA"]) * df_node_local["awarded"]
    df_node_local["rules"] = ' & '.join([str(rule) for rule in strategy.rules])

    return df_node_local


if __name__ == "__main__":
    # Load the virtual trading data
    node_data = get_node_data("BONETSLR_RN")
    # Define the strategy
    rules = [TimeBasedRule(day_of_week='Tuesday', hour_range=list(range(0, 12)))]
    strategy = Strategy("BONETSLR_RN", rules)
    # Evaluate the strategy
    results = evaluate_performance(node_data, strategy)
    # To save replace -inf with -999
    results = results.replace(-float('inf'), -999)
    results.to_csv("../results/nodo_BONETSLR_RN.csv")
