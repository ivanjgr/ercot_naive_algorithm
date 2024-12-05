import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from os.path import join




class Results:
    __FILE_PATH__ = os.path.dirname(__file__)

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.spp_name = df['settlementPoint'].unique()[0]

    def save_results(self):
        parent_folder = os.path.dirname(self.__FILE_PATH__)
        self.df.to_csv(join(parent_folder, 'results', 'csv', f'{self.spp_name}_results.csv'))

    def generate_plot(self):
        parent_folder = os.path.dirname(self.__FILE_PATH__)

        fig, ax = plt.subplot_mosaic([['profit', 'mw'], ['SPP', 'SPP']], figsize=(12, 8), tight_layout=True)
        self.df["cum_profit"] = self.df["profit"].cumsum()
        self.df["mw"] = self.df["awarded"].cumsum()
        self.df.plot(y='cum_profit', ax=ax['profit'], label='Cumulative profit')
        ax['profit'].grid(linestyle='--', linewidth=0.5, color='gray', alpha=0.5)
        ax['profit'].axhline(0, color='red', linestyle='-', linewidth=0.5)
        ax['profit'].set_ylabel('USD')
        ax['profit'].get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

        ax['mw'].plot(self.df.index, self.df['bid_price'], color='blue')
        # Configure axis between the 10th and 90th percentile
        ax['mw'].set_ylim(self.df['bid_price'].quantile(0.02), self.df['bid_price'].quantile(0.98))
        # Grid
        ax['mw'].grid(linestyle='--', linewidth=0.5, color='gray', alpha=0.5)
        # log axis
        self.df.plot(y='SPP_DA', ax=ax['SPP'])
        self.df.plot(y='SPP_RT', ax=ax['SPP'])
        ax['SPP'].grid(linestyle='--', linewidth=0.5, color='gray', alpha=0.5)
        ax['SPP'].set_ylabel('USD')
        ax['SPP'].set_ylim(self.df['SPP_DA'].quantile(0.02), self.df['SPP_DA'].quantile(0.98))

        plt.suptitle(f"{self.spp_name}")
        plt.savefig(join(parent_folder, 'results', 'img', f'{self.spp_name}_results.png'), dpi=300, bbox_inches='tight')
        plt.close()

    def __str__(self):
        str_results = f"Results for node {self.spp_name}:\n"
        #rules = self.df['rules'].unique()
        #str_results += f"\tRules: {rules}\n"
        total_return = self.df['profit'].sum()
        str_results += f"\tTotal profit: USD {total_return:,.2f}\n"
        total_losses = self.df[self.df['profit'] < 0]['profit'].sum()
        str_results += f"\tTotal losses: USD {total_losses:,.2f}\n"
        n_hours_awarded = self.df['awarded'].sum()
        str_results += f"\tTotal hours awarded: {n_hours_awarded}\n"
        average_return = self.df['profit'].mean()
        roi = total_return / self.df[self.df.awarded == 1]['SPP_DA'].sum()
        str_results += f"\tAverage return: USD {average_return:,.2f}\n"
        str_results += f"\tROI: {roi*100:.2f}%\n"

        return str_results
