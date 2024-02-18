import numpy as np
import decimal

def normalize(arr):
    arr = [decimal.Decimal(num) for num in arr]
    total = sum(arr)
    return [num/total for num in arr]

def portfolio_weights(rate, expected_roi_per_stock):
    length = len(expected_roi_per_stock)

    # Create a numpy array with the given length, filled with the values 1, rate, rate^2, ..., rate^(length-1)
    arr = np.array([rate ** i for i in range(length)])

    # Modify weights based on return. Convert all negative expected_roi_per_stock weights to 0 since we obviously
    # don't want to put money into them
    expected_roi_per_stock = np.where(expected_roi_per_stock <= 0, 0, expected_roi_per_stock)
    arr = arr * expected_roi_per_stock

    # Find the number of stocks you are investing into
    num_stocks_invested_into = len(expected_roi_per_stock) - np.count_nonzero(expected_roi_per_stock == 0)

    if num_stocks_invested_into != 0:
        # Normalize the array so that the elements sum to 1
        arr = normalize(arr)

        # Make sure it sums to 1
        PRECISION = 15
        arr = [round(num, 10).quantize(decimal.Decimal("0."+"0"*PRECISION)) for num in arr]
        difference = 1 - sum(arr)
        arr[0] = arr[0] + difference

        # Check it sums to 1
        if sum(arr) != 1:
            raise ValueError(f"Array does not sum to 1. It sums to {sum(arr)}")
    else:
        # For consistency, turn zeros-array into a list too
        arr = [decimal.Decimal(num) for num in arr]

    return arr, num_stocks_invested_into


def rois_func(tup):
    rate, portfolio_data = tup
    port_index = portfolio_data.index
    length = port_index.unique().shape[0]
    rois = np.zeros((length, 4))
    for i, date in enumerate(port_index.unique()):
        # sort by predicted ROI
        current_df = portfolio_data.loc[date, :]

        # Get array containing predicted ROI for each stock
        expected_roi_per_stock = ((current_df["predicted prices"].values - current_df["current price"].values) /
                                  current_df["current price"].values) * 100
        current_df["predicted ROI"] = expected_roi_per_stock

        current_df = current_df.sort_values(["predicted ROI"], ascending=False)

        weights, num_stocks = portfolio_weights(rate, current_df["predicted ROI"].values)

        current_portfolio_wealth = sum([weights[w] * decimal.Decimal(current_df["current price"][w]) for w in range(len(weights))])
        current_portfolio_wealth = float(current_portfolio_wealth)
        if current_portfolio_wealth != 0:
            future_true_wealth = sum([weights[w] * decimal.Decimal(current_df.loc[:, "true prices"][w]) for w in range(len(weights))])
            future_true_wealth = float(future_true_wealth)

            future_predicted_wealth = sum([weights[w] * decimal.Decimal(current_df.loc[:, "predicted prices"][w]) for w in range(len(weights))])
            future_predicted_wealth = float(future_predicted_wealth)

            if future_true_wealth < 0:
                raise ValueError(
                    f"Future true wealth can't be less than 0 but it is: {future_true_wealth}\n"
                    f"and the weights are:\n"
                    f"{weights}\n"
                    f"which sum to: {sum(weights)}")

            true_roi = ((future_true_wealth - current_portfolio_wealth) / current_portfolio_wealth) * 100
            expected_roi = ((future_predicted_wealth - current_portfolio_wealth) / current_portfolio_wealth) * 100

            rois[i, :] = np.array([rate, true_roi, expected_roi, num_stocks])
        else:
            # Whenever all stocks are expected to decrease in value the following is added instead. True ROI and
            # predicted ROI cannot be calculated due to divide by zero error.
            rois[i, :] = np.array([rate, np.nan, np.nan, np.nan])
    return rois
