import os
import itertools
import numpy as np
import pandas as pd
from utils import get_texas_season

FILE_PATH = os.path.dirname(__file__)


def get_node_data(settlement_point_name: str) -> pd.DataFrame:
    """
    Get the virtual trading data for a specific node
    :param settlement_point_name: Name of the settlement point
    :return: DataFrame with the virtual trading data for the node
    """
    parent_folder = os.path.dirname(FILE_PATH)
    DATA_PATH = os.path.join(parent_folder, 'data')
    virtual_trading_data = pd.read_csv(os.path.join(DATA_PATH, 'virtual_trading_data.csv'))
    node_data = virtual_trading_data[virtual_trading_data['settlementPoint'] == settlement_point_name].copy()
    # Add common fields (day_of_week, hour, month_name, etc)
    node_data["date"] = pd.to_datetime(node_data["date"])
    node_data["day_of_week"] = node_data["date"].dt.day_name()
    node_data["hour_ending"] = node_data["date"].dt.hour + 1
    node_data["month_name"] = node_data["date"].dt.month_name()
    # Season
    node_data["season"] = node_data["date"].dt.quarter.map({1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'})
    node_data = node_data.set_index("date")

    return node_data


class Strategy:
    def __init__(self, settlement_point_name: str, rules: list):
        self.settlement_point_name = settlement_point_name
        self.node_data = get_node_data(settlement_point_name)
        self.rules = rules

        self.min_margen = 5

    def get_offer_price(self, operation_date: pd.Timestamp):
        # For now the bid price will be the RTM price avg - self.min_margin from two days before the same hour
        # RTM price avg from from 1 week
        two_days_ago_date = operation_date - pd.Timedelta(days=2)
        one_week_ago_date = operation_date - pd.Timedelta(days=7)
        bid_price = self.node_data.loc[one_week_ago_date:two_days_ago_date, "SPP_RT"].mean() - self.min_margen

        return bid_price

    def apply_rules(self, operation_date: pd.Timestamp):
        # If none of the rules apply, return -inf
        if not all([rule.is_applicable(operation_date) for rule in self.rules]):
            return -np.inf

        return self.get_offer_price(operation_date)


class TimeBasedRule:
    def __init__(self, day_of_week: str, hour_range: list, season: str = None):
        self.day_of_week = day_of_week
        self.hour_range = hour_range
        self.season = season


    def is_applicable(self, date_time: pd.Timestamp):
        if self.season:
            return all([date_time.day_name() == self.day_of_week,
                        date_time.hour in self.hour_range,
                        get_texas_season(date_time) == self.season])
        else:
            return date_time.day_name() == self.day_of_week and date_time.hour in self.hour_range

    def __str__(self):
        # Super compressed representation
        # See if there are any consecutive hours and represent them as a range
        h_ranges = []
        for k, g in itertools.groupby(enumerate(self.hour_range), lambda ix: ix[0] - ix[1]):
            g = list(g)
            if len(g) > 1:
                h_ranges.append((g[0][1], g[-1][1]))
            else:
                h_ranges.append(g[0][1])

        return f"{self.day_of_week[:3]}, {h_ranges})"
