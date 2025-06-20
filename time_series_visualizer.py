import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col=['date'])

# Clean data
lower_pageviews_threshold = df['value'].quantile(0.025)
higher_pageviews_threshold = df['value'].quantile(0.975)
df = df[(df['value'] >= lower_pageviews_threshold) & (df['value'] <= higher_pageviews_threshold)]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 5))

    df.plot(
        ax = ax,
        kind = 'line',
        title ='Daily freeCodeCamp Forum Page Views 5/2016-12/2019',
        y = 'value',
        xlabel = 'Date',
        ylabel = 'Page Views', 
        color ='red',
        legend = False
    )

    # Save image and return fig
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    missing_data = pd.DataFrame(
        data=[
            ['2016', 'January', 0], 
            ['2016', 'February', 0],
            ['2016', 'March', 0], 
            ['2016', 'April', 0]],
        columns=['year', 'month', 'value']
    )

    # Combine data
    df_combined = pd.concat([missing_data, df_bar], ignore_index=True, sort=False)
    df_combined['year'] = pd.to_numeric(df_combined['year'], errors='coerce').astype('Int64')

    # Aggregate
    df_agg = df_combined.groupby(['year', 'month'], sort=False).mean(numeric_only=True).reset_index()

    # Pivot for grouped bar plot
    df_pivot = df_agg.pivot(index='year', columns='month', values='value')

    # Ensure months are in correct order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    df_pivot = df_pivot[month_order]

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(8, 8))
    df_pivot.plot(
        ax=ax,
        kind='bar',
        ylabel='Average Page Views',
        xlabel='Years'
    )
    plt.legend(title='Month')

    # Save image and return fig
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    sns.boxplot(ax=axs[0], x='year', y='value', data=df_box)
    axs[0].set_title('Year-wise Box Plot (Trend)')
    axs[0].set_xlabel('Year')
    axs[0].set_ylabel('Page Views')

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    sns.boxplot(ax=axs[1], x='month', y='value', data=df_box, order=month_order) 
    axs[1].set_title('Month-wise Box Plot (Seasonality)')
    axs[1].set_xlabel('Month')
    axs[1].set_ylabel('Page Views')

    # Save image and return fig 
    fig.savefig('box_plot.png')
    return fig
