from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.optimize import curve_fit


def exp_recovery(t: np.ndarray, Ifinal: float, A: float, k: float) -> np.ndarray:
    """
    Exponential decay function for curve fitting.

    use https://www.desmos.com/calculator/bvitqijgd6 to visualize the fit

    :param t: Time points, x-axis values
    :param A: Amplitude of the exponential decay
    :param k: Decay constant
    :param Ifinal: Final intensity value (asymptote / plateau)
    """

    return Ifinal - A * np.exp(-k * t)


INPUT_FILEPATH = Path(
    '../../../data/viral_condensates/hsv1/ul49/UL49 GFP FRAP02/UL49 GFP FRAP02.csv'
)


df = pd.read_csv(
    INPUT_FILEPATH,
    skiprows=1,
    encoding='utf-16',
    index_col=0,
)

df.columns = df.columns.str.strip('[] ')

# find last and last row number of all NULL rows
null_row_index = df[df.isnull().all(axis=1)].index[0]
last_null_row_index = df[df.isnull().all(axis=1)].index[-1]
null_row_number = df.index.get_loc(null_row_index)
last_null_row_number = df.index.get_loc(last_null_row_index)

df_prebleach = df.iloc[:null_row_number]
df_postbleach = df.iloc[last_null_row_number + 1:]
df_prebleach_means = df_prebleach.mean()
df_prebleach_norm = df_prebleach / df_prebleach_means
df_postbleach_norm = df_postbleach / df_prebleach_means

# df_prebleach
# df_postbleach

for roi in df.columns:
    # take initial guess for parameters [Ifinal, A, k]
    # fit the data to the exp_recovery function
    # get the fitted parameters from the curve_fit
    initial_guess = [1, 1, 0.1]  # [Ifinal, A, k=]
    xdata = df_postbleach_norm[roi].index.values
    ydata = df_postbleach[roi].values
    ydata_norm = df_postbleach_norm[roi].values

    params: tuple[float, float, float]
    params, _covariance = curve_fit(
        f=exp_recovery,
        xdata=xdata,
        ydata=ydata_norm,
        p0=initial_guess,
        maxfev=5000,
    )

    ydata_fitted = exp_recovery(xdata, *params)

    Ifinal, A, k = params
    Ipre = df_prebleach_norm[roi].mean()
    Ipost = df_postbleach_norm[roi].min()
    mobile_fraction = (Ifinal - Ipost) / (Ipre - Ipost)
    mobile_fraction_x = df_postbleach_norm[roi].index[(df_postbleach_norm[roi] - Ifinal).abs().argmin()]

    xdata_combined = np.concatenate((df_prebleach[roi].index.values, xdata))
    ydata_norm_combined = np.concatenate((df_prebleach_norm[roi].values, ydata_norm))
    # ydata_std = df_postbleach_norm[ROI].std()
    ymin = df_postbleach_norm[roi].min()

    sns.set_theme(style='ticks', palette='colorblind')
    sns.scatterplot(
        x=xdata_combined,
        y=ydata_norm_combined,
        label='Normalized Data',
    )
    sns.lineplot(
        x=xdata,
        y=ydata_fitted,
        label='Exponential Fit',
        color='orange',
    )
    plt.vlines(
        x=mobile_fraction_x,
        ymin=ymin,
        ymax=Ifinal,
        color='g',
        linestyle='--',
        label=f'Mobile Fraction: {mobile_fraction:.2%}',
    )
    # plt.text(
    #     x=mobile_fraction_x,
    #     y=(Ifinal + ymin) / 2,
    #     s=f'  {100 * mobile_fraction:.2f}%',
    #     color='g',
    # )
    plt.hlines(
        y=ymin,
        xmin=0,
        xmax=xdata[-1],
        color='r',
        linestyle='--',
        label='Post Intensity',
    )
    plt.hlines(
        y=Ifinal,
        xmin=0,
        xmax=xdata[-1],
        color='r',
        linestyle='-.',
        label='Final Intensity',
    )
    plt.ylim(top=1)
    plt.xlabel('Time [sec]')
    plt.ylabel('Normalized Intensity [%]')
    plt.legend(
        # loc='center left',
        # bbox_to_anchor=(1, 0.5),
        # fontsize='small',
        prop={
            'size': 7,
        },
    )

    plt.title(f'FRAP Recovery with Exponential Fit\n{INPUT_FILEPATH.stem} ({roi})')
    plt.show()
