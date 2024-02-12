# Future Stock Price Prediction

## Objective
The primary objective of this project is to explore the feasibility of creating a model capable of predicting the price of a stock (roughly*) one year into the future for the top 1000 companies in the US by market capitalisation. The ultimate aim is to construct profitable stock portfolios based on these predictions. An additional aspect of this project is to assess the impact of incorporating leading and lagging economic indicators of the US from OECD data on the prediction performance.

## Results
Ultimately, it is clear from the plot `results/overview/results (loss).html` that models which use economic indicators to inform their predictions perform better. Specifically, the best-performing model, which integrates these indicators, achieved a lower loss of 15.45 on the test set compared to 16.14 for the baseline model that did not utilize economic indicators. This represents a 4.27% improvement in model accuracy, underscoring the value of economic data in enhancing predictive reliability. The best model produced profitable portfolios on the test set roughly 68% of the time. The portfolios this model generated in the training, validation and test set (along with their performance) are visualised in `results/best_model_portfolios.html`. For context, the test set had data from 24/07/2017 to 27/06/2022 which consists of 3 primary bear markets with each one followed by a relatively strong bull market. Therefore, the test set is relatively diverse. However, I would still recommend further analysis incorporating cross-validation to further assess the capability of the model in creating profitable portfolios in many different states of the economy and stock market. 

## Explanation of project:
1. "Data creation" notebook
	- Downloaded stock price data from yfinance library of top 1000 companies in the US by market capitalisation along corresponding sector data
	- Downloaded chosen lagging and leading economic indicators data of the US from OECD data
	- The stock price has daily frequency and economic indicators have monthly frequency. Resampled and combined these into one dataframe with daily frequency data.
2. "Data exploration" notebook
	- Explored the rate of data drop-off as you get closer to 1980 (as many of these companies didn't even exist back then)
	- Visualised the features and stock price data using line plots to ensure everything looks normal
	- To assist with feature selection:
		- Created correlation matrix 
		- Created scatter plot to show stock price against a chosen economic indicator and examined them for any relationship
3. "Creating models" notebook
	- Experimented with several models with different hyperparameters which affect both the data used to train the model and also the model structure itself. Experimented with models using various combinations of features using earlier feature selection visualisations as a guide
	- This notebook also saves all the models into a folder (results/details/models)
	- It also plots for the models' training (loss per epoch) and also saves these plots into a folder too ("results/details/training & validation details")
	- Also records the results (val loss, val r-squared) along with hyperparameters used in a csv (results/overview/model results.csv)
4. "Best model" notebook
	- Used results in "model results.csv" in order to create 2 plots showing validation loss and validation r-squared against model hyperparameters (results/overview/results (r2).html & results/overview/results (loss).html) 
	- Chose the best model based on these 2 plots considering validation loss, validation r-squared and also simplicity of the model
	- Then explored how this models perform in terms of creating profitable portfolios:
		- A portfolio is created for every day in the data. The portfolio consists of stocks which the model believe will go up in value. The parameter `rate` determine what proportion of the portfolio a particular stock will make up. Smaller `rate` means less diverse portfolio and higher `rate` means more diverse portfolio.
		- Many different rates are explored via the boxplot which plots return on investment (ROI) on the portfolios against rates
		- After a rate is chosen, a more detailed plot (results/best_model_portfolios.html) is created which plots the predicted ROI of portfolios against the actual ROI of the portfolios (with more information available upon hovering over the points) 

## Caveats
- The prediction is for approximately 530 days into the future from the current date, equating to around 365 weekdays as the market is closed on weekends
- The `price.csv` file, essential for the project, is too large for direct upload. Therefore, a zipped version is included in the repository. Users must unzip this file to ensure the proper functioning of the project components. Alternatively, users can run the `1-Data creation.ipynb` notebook, which employs the `yfinance` library to generate the `price.csv` file. However, this process may be time-consuming due to the volume of data to be downloaded.
