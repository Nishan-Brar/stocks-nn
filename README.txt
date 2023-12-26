# Future Stock Price Prediction

## Goal
The primary objective of this project is to explore the feasibility of creating a model capable of predicting the price of a stock (roughly) one year into the future. The ultimate aim is to construct profitable stock portfolios based on these predictions. An additional aspect of this project is to assess the impact of incorporating leading and lagging economic indicators from OECD data on the prediction performance.

## Results
The results of the best performing model are available in the `results/overview` directory as an HTML file. This file (generated using the Plotly library) showcases all the portfolios created by the AI from the training and testing data with their expected return on investment (ROI) against their actual ROI. Contrary to initial assumptions, the inclusion of economic indicators from OECD data did not significantly enhance the model's performance in predicting stock prices.

## Caveats
- The prediction is for approximately 530 days into the future from the current date, equating to around 365 weekdays as the market is closed on weekends
- The `price.csv` file, essential for the project, is too large for direct upload. Therefore, a zipped version is included in the repository. Users must unzip this file to ensure the proper functioning of the project components. Alternatively, users can run the `1-Data creation.ipynb` notebook, which employs the `yfinance` library to generate the `price.csv` file. However, this process may be time-consuming due to the volume of data to be downloaded.
