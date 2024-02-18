# Future Stock Price Prediction
Website: https://blue-goby-nzj8.squarespace.com/?password=nishan

## Objective
With the ultimate goal of constructing profitable stock portfolios, this project investigates the feasibility of building a model to predict the price of the top 1000 US companies by market cap 1.5 years ahead. The project will also assess the impact of including leading and lagging economic indicators from OECD data on the model's predictive power.

## Results
Ultimately, it is clear from the plot `results/overview/results (loss).html` that models which use economic indicators to inform their predictions perform better. Specifically, the best-performing model, which integrates these indicators, achieved a lower loss of ____________ on the test set compared to a loss of ____________ for the best baseline model (which don't use economic indicators). This represents a _______________% improvement in model accuracy, underscoring the value of economic data in enhancing predictive reliability. The best model produced profitable portfolios on the test set roughly _____________ of the time. The portfolios this model generated in the test set (along with their performance) are visualised in `results/best_model_portfolios.html`. For context, the test set had data from 24/07/2017 to 27/06/2022 which consists of 3 primary bear markets with each one followed by a relatively strong bull market. Therefore, the test set is relatively diverse. However, I would still recommend further analysis incorporating cross-validation to further assess the capability of the model in creating profitable portfolios in many different states of the economy and stock market. 

## Usage Instructions
The `price.csv` file, essential for the project, is too large for direct upload. Therefore, a zipped version is included in the repository. Users must unzip this file to ensure the proper functioning of the project components. Alternatively, users can run the `1-Data creation.ipynb` notebook, which employs the `yfinance` library to generate the `price.csv` file. However, this process may be time-consuming due to the volume of data to be downloaded.

## Explanation of project notebooks:

1. **1 - Data Collection and Preprocessing.ipynb**
   - This notebook initiates the project by collecting stock price data and economic indicators for the top 1000 US companies by market cap using the `yfinance` library and OECD data, respectively. It covers the preprocessing steps such as handling missing values, aligning data frequencies (daily for stock prices, monthly for economic indicators) and consolidating them into a single dataset ready for analysis.

2. **2 - Exploratory Data Analysis and Visualization.ipynb**
   - Focuses on exploring the collected data to understand its characteristics and patterns. It includes the visualization of stock price trends, data availability over time and the relationship between stock prices and economic indicators. The notebook also employs statistical techniques to identify potential correlations useful for feature selection.

3. **3 - Model Development.ipynb**
   - Dedicated to building and evaluating predictive models. It explores various architechtures for neural networks, adjusting hyperparameters and incorporating different subsets of features based on insights from the previous exploratory analysis. The notebook systematically records model performance, visualizes training processes and lays the groundwork for selecting the optimal model based on validation loss and validation R-squared.

4. **4 - Optimal Model Selection and Portfolio Analysis.ipynb**
   - This notebook concludes the modeling phase by comparing different models' performance to select the best one. It then moves beyond individual stock predictions to assess how these forecasts can be leveraged to construct profitable stock portfolios. It involves simulating portfolio returns under different configurations and selecting the best strategy based on ROI and risk considerations.

## Caveat
- The prediction is for 365 weekdays into the future which is approximately 1.5 years into the future from the current date. This is because the market is closed on weekends.
