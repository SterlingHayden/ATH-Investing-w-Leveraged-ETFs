# Investing at All-Time Highs (ATH) 📊

**J.P. Morgan Asset Management** reports that buying at ATHs in popular ETFs like the **S&P 500** has minimal impact on long-term performance. In fact, history shows investors can benefit from investing at ATHs rather than waiting for a dip.

<img src="https://www.jpmorgan.com/content/dam/jpmorgan/images/jpma/3-considerations-for-investing-in-a-bull-market/3-considerations-for-investing-in-a-bull-market-chart-3.jpg" alt="ATH Performance Chart" width="550"/>

More details can be found [here](https://www.jpmorgan.com/insights/markets/top-market-takeaways/3-considerations-for-investing-in-a-bull-market#:~:text=Over%2024%20months%2C%20an%20individual,return%20an%20average%20of%2018.5%25).
  

# How Does Investing in Leveraged ETFs at or near All-Time Highs or 52 Week Highs Compare?
This repository aims to provide a reproducible answer to that question. By simulating historical leveraged data and backtesting return rates, it seeks to analyze the risks and rewards of investing in leveraged portfolios during market highs in a reproducible manner.  

| File                             | What it does                                                                                                                |
|----------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| `Demo-Single-Stock.ipynb`        | Simulates and backtests the return rates of a **single stock** selected by the user.                                        |
| `Demo-Portfolio.ipynb`           | Simulates and backtests the return rates of a **porfolio of stocks** selected by the user.                                  |
| `utilities.py`                | Provides callable functions for data preprocessing, return calculations, and plotting.                                      |
  
$~$. 
  
# Key Findings
⭐ Backtesting with leveraged Shiller data from the 1800s reveals that historically, investing at or near 52-week highs has been less risky and more stable compared to investing at or near all-time highs.

⭐ Leveraging a portfolio of stocks reduces risk compared to leveraging a single stock.

⭐ Investing at an all-time high in portfolio price carries more momentum than investing at a 52-week high.  

$~$

## **Leveraged Single Stock Returns**
### Applying a 3x leverage multiplier to the daily returns of $SPY, equivalent to $UPRO.
| When Buying On or Near an All-Time High                 | When Buying On or Near a 52-Week High                 |
|---------------------------------------------------------|-----------------------------------------------------------|
| ![Plot ATH](example-images/3X-SPY-ATH.png) | ![Plot 52W](example-images/3X-SPY-52W.png) |

### Similarly to above we can apply a 2x leverage multiplier to the daily returns of $SPY, equivalent to $SPUU.
| When Buying On or Near an All-Time High                 | When Buying On or Near a 52-Week High                 |
|---------------------------------------------------------|-----------------------------------------------------------|
| ![Plot ATH](example-images/2X-SPY-ATH.png) | ![Plot 52W](example-images/2X-SPY-52W.png) |

### We can visualize the All-Time High returns with side-by-side charts comparing 3X leveraged and unleveraged performance, using the same high-point buy strategy but with different purchase timings for leveraged and unleveraged cases.
![Plot ATH PR](example-images/3X-SPY-ATH-PR.png)


### If we’re concerned that the simulated timeframe isn’t representative, we could use [Shiller Data](http://www.econ.yale.edu/~shiller/data.htm), which includes historical returns for large-cap U.S. stocks such as the S&P 500, dating back to the 1800s. This would help us better understand how leveraging the S&P 500 performs across various market conditions. The following plots are 3X leveraged.
| When Buying On or Near an All-Time High                 | When Buying On or Near a 52-Week High                 |
|---------------------------------------------------------|-----------------------------------------------------------|
| ![Plot ATH](example-images/3X-Shiller-ATH.png) | ![Plot 52W](example-images/3X-Shiller-52W.png) |


### When backtesting with Shiller data, we find that investing at or near all-time highs performs poorly, whereas buying at 52-week highs shows stronger outcomes. Let’s now examine how leveraged and unleveraged performance compares over our holding periods of interest (e.g., 1–2 years).
![Plot 52W PR](example-images/3X-Shiller-52W-PR.png)

$~$

## **Leveraged Portfolio of Stock Returns**
### Applying a 3x leverage multiplier to the daily returns of $QQQ, $SPY, and $SOXX (equivalent to $TQQQ, $UPRO, and $SOXL), with $TQQQ representing 60% of the portfolio, $UPRO 20%, and $SOXL 20%.
| When Buying On or Near an All-Time High                 | When Buying On or Near a 52-Week High                 |
|---------------------------------------------------------|-----------------------------------------------------------|
| ![Plot ATH](example-images/Portfolio-ATH.png) | ![Plot 52W](example-images/Portfolio-52W.png) |

### The return spread appears similar in the [side-by-side charts comparing leveraged and unleveraged performance](example-images/Portfolio-ATH-PR.png), with the unleveraged portfolio outperforming on average until the 4-year mark, after which the leveraged portfolio takes the lead.
![Plot ATH PR 1y-2y](example-images/Portfolio-ATH-PR-1y-2y.png)
![Plot ATH PR 4y](example-images/Portfolio-ATH-PR-4y.png)
