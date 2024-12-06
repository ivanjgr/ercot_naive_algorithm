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

        # Histograma de la suma de los retornos, incluyendo los negativos
        skew = self.df[['return_DA_RT']].resample('D').sum().skew().values[0]
        df_no_outliers = self.df[["return_DA_RT"]].resample('D').sum()
        df_no_outliers = df_no_outliers[np.abs(df_no_outliers['return_DA_RT'] - df_no_outliers['return_DA_RT'].mean()) <= (3 * df_no_outliers['return_DA_RT'].std())]
        df_no_outliers.hist(
            ax=ax['mw'],
            color='blue',
            alpha=0.5,
            edgecolor='black', linewidth=0.5,
            label='Return DA-RT',
            bins=40
        )
        # No title for ax['mw']
        ax['mw'].set_title('Daily return DA-RT, excluding outliers')
        # Add skew as text in the plot
        ax['mw'].text(0.95, 0.95, f"Skew: {skew:.2f}", transform=ax['mw'].transAxes, fontsize=10,
                      verticalalignment='top', horizontalalignment='right')
        # Thousand separator for x axis
        ax['mw'].get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

        # Daily mean SPP
        self.df[["SPP_DA"]].resample('D').mean().plot(y='SPP_DA', ax=ax['SPP'], linewidth=0.5, color='green')
        self.df[["SPP_RT"]].resample('D').mean().plot(y='SPP_RT', ax=ax['SPP'], linewidth=0.5, color='red')
        ax['SPP'].grid(linestyle='--', linewidth=0.5, color='gray', alpha=0.5)
        ax['SPP'].set_ylabel('USD')

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
