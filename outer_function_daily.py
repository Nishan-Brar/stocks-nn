from numba import jit
import numpy as np


@jit(nopython=True, parallel=False)  # Runs better with parallel = False for some reason.
def estimate_slope(x, y):
    # number of observations/points
    n = len(x)

    # mean of x and y vector
    m_x = np.mean(x)
    m_y = np.mean(y)

    # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y * x) - n * m_y * m_x
    SS_xx = np.sum(x * x) - n * m_x * m_x

    # calculating regression coefficients
    b_1 = SS_xy / SS_xx

    return b_1  # return only slope


def inner_function(i, NUMBER_OF_LINES, filtered_dates_and_stocks_np, price_after_one_year, current_prices):
    column_array = filtered_dates_and_stocks_np[:, i]
    splits = np.array_split(column_array, NUMBER_OF_LINES)

    slopes_roi = np.zeros(NUMBER_OF_LINES + 2)
    for j in range(NUMBER_OF_LINES):
        x = np.arange(len(splits[j]))
        slopes_roi[j] = estimate_slope(x, splits[j])

    # add expected price
    slopes_roi[-1] = price_after_one_year[i]

    # add current price.
    # NOTE THAT THE CURRENT PRICE IS EXPECTED TO BE THE SECOND LAST COLUMN OF THE WHOLE DATA SET IN OTHER PARTS OF THE
    # CODE !!
    slopes_roi[-2] = current_prices[i]

    return slopes_roi


# This function goes through a particular "row" of the data. Where the "row" indexed by `d` represents the
# "last date" in the current data being considered.
def outer_function(d, stocks_np, NUMBER_OF_YEARS_TO_CONSIDER, NUMBER_OF_LINES, features_subset_indexes, features_np,
                   cats_np, cats_index, cats_df, dates, stocks):
    # `-1` needed as `+1` is in original notebook due to slicing being end-exclusive
    current_date = dates[d-1]

    # Filter "dates". We want current date and the next `NUMBER_OF_YEARS_TO_CONSIDER`. We also need to filter
    # `features_np` accordingly.
    # `-1` needed as `+1` is in original notebook due to slicing being end-exclusive
    starting_index = d - 365 * NUMBER_OF_YEARS_TO_CONSIDER - 1
    filtered_dates_stocks_np = stocks_np[starting_index:d, :]

    # Get price of all stocks after 1 year after `d`. `+365` to calculate roi after a year. `+1` not needed anymore as
    # that was for end-element exclusive for slicing.
    # `-1` needed as `+1` is in original notebook due to slicing being end-exclusive
    price_after_one_year = stocks_np[d + 365 - 1, :]

    # Now we drop any columns containing NaN value(s)
    booleans = ~np.isnan(filtered_dates_stocks_np).any(axis=0)
    filtered_dates_and_stocks_np = filtered_dates_stocks_np[:, booleans]
    stocks = stocks[booleans]
    # We also need to drop these columns from `cats_np`
    filtered_cats_np = cats_np[:, booleans]
    # Filter `price_after_one_year` to only include end stock price of stocks in `filtered_dates_and_stocks_np`
    price_after_one_year = price_after_one_year[booleans]

    # Now we check if there are any nan in `price_after_one_year` and also remove corresponding columns from
    # `filtered_dates_and_stocks_np`
    booleans = ~np.isnan(price_after_one_year)
    price_after_one_year = price_after_one_year[booleans]
    filtered_dates_and_stocks_np = filtered_dates_and_stocks_np[:, booleans]
    stocks = stocks[booleans]
    # We also need to drop these columns from `cats_np`
    filtered_cats_np = filtered_cats_np[:, booleans]

    # Get current prices
    current_prices = filtered_dates_and_stocks_np[-1, :]

    # Create data row by row
    iters = range(filtered_dates_and_stocks_np.shape[1])

    # Store rows
    cats_dict = dict()
    cats_df = cats_df.iloc[:, cats_index]
    for k, category in zip(cats_index, cats_df.columns):
        cats_dict[k] = np.empty(filtered_dates_and_stocks_np.shape[1], dtype=int)

    features_dict = dict()
    for k in features_subset_indexes:
        features_dict[k] = np.zeros((filtered_dates_and_stocks_np.shape[1], 1))

    row_storage = np.zeros((filtered_dates_and_stocks_np.shape[1], NUMBER_OF_LINES + 2))
    # This goes through the columns
    for i in iters:
        # `-1` needed as `+1` is in original notebook due to slicing being end-exclusive
        features = features_np[d - 1, features_subset_indexes]
        row = inner_function(i, NUMBER_OF_LINES, filtered_dates_and_stocks_np, price_after_one_year, current_prices)

        # Get each stock's corresponding categorical variables.
        cats = filtered_cats_np[cats_index, i]

        # The last category is the base category so the array should just be all 0s if this stock has a base category
        # for any categorical variable.
        for (c, cat), k in zip(enumerate(cats), cats_index):
            series = cats_df.iloc[:, c].dropna()
            index = series[series == cat].index[0]
            cats_dict[k][i] = index

        for feature, k in zip(features, features_subset_indexes):
            features_dict[k][i, 0] = feature

        row_storage[i, :] = row

    row_store_dates = [current_date] * len(row_storage)
    return row_storage, row_store_dates, stocks, cats_dict, features_dict
