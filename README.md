# K_Mean_Fundamentals (QFRM!!!)

## Motivation
Traditional stock clustering methods rely on a hollistic approach to evaluate stocks, e.g. GICS, BICS that groups stocks based on fundamentals and type of business.

Traditional value investment also puts great emphasis on firm characteristics (FCs) to seperate good stocks and bad stocks, and we would pose some issues regarding the traditional method:
* Traditional factors are too simple, e.g. HML (Book to market ratios), SMB (Market cap), MOM (Past return), etc., which only rank stocks using one FC. Can we increase the **dimension from one to more**?
* Can we split the stock analysis process into different parts by looking into different subset of FCs, and for each subset, generate a strategy **without any prior knowledge on FCs outside this subset**?

For the second issue, within normal heuristic rules, when we are provided only a subset of firm characteristics (FCs), e.g. only data from income statement is provided, it is not easy to find clustering rules to have the most similarities within clusters.

## Our approach
We will seperate stock analysis into different groups of FC (one FC can be placed in more than one group), group examples are as follows:

* Operating Profitability Ratios (Operating Margin, Earnings Margin, ROI, ROE, etc.)
* Financial Risk (Debt Equity Ratio, Interest Coverage Ratio, etc.)
* Business Risk (Operating Leverage, Total Leverage, etc.)
* Turnover Ratio (Inventory Turnover, Receivable Turnover Ratio, etc.)
* Market Related Information (EV/EBITDA, P/E, etc.)

Within each group, we will run a K-mean clustering on stocks. Plot the result in scatter plot, pick FCs that show significancy in splitting the stocks, then re-train the results with the selected FCs using a multi-class logistics regression to tune parameteres that cluster the stocks.

By looking at the time series return of the clusters, we will check if there is possibilities of forming a Long-Short portfolio to generate a stable return.

Finally, we propose to combine all LS portfolios into one LS portfolio, so we end up getting back to a hollistic evaluation of a stock, with clearer decision making for each group of FC.








