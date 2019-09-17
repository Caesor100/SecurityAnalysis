# SecurityAnalysis
___The application is under development___.

The program allows you to obtain an assessment of the financial statements of the company.

![image](https://user-images.githubusercontent.com/31075923/64907484-ac751380-d6fb-11e9-82c9-b55e17e54c83.png)

### program start
_On Windows_

Activate virtual environment
```sh
> venv\Scripts\activate
```
Program start
```sh
> python security_analysis.py
```

### Financial indicators are evaluated on a five-point scale:
* 5/5 - good
* 4/5 - normal
* 3/5 - below normal
* 2/5 - bad
* 1/5 - vary badly

## Financial performance measurement system
### Gross margin
Gross margin = (gross profit / revenue) * 100%
 * gross margin >= 40%: good
 * 40% > gross margin >= 35%: normal
 * 35% > gross margin >= 30%: below normal
 * 30% > gross margin >= 25%: bad
 * gross margin < 25%: very badly
 
### Selling, General and Administrative Expenses (SG&A)
rSG%A - (SG&A / gross profit) * 100 %
X - arithmetic mean rSG&A
Sigma - Standard deviation rSG&A
V = (sigma/X) * 100 % - coefficient of variation rSG%A

__The most important key factor in SG&A performance is stability. In other words, **_coefficient of variation rSG%A_** must be greater than 30%.__

When 65 > X > 25
* V <= 30 %: good
* 35% => V > 30 %: normal
* 40% => V > 35 %: below normal
* 45% => V > 40 %: bad
* V > 45 %: bad
---
When 65 < X < 25
* V  <= 30 %: normal
* 35% >= V > 30%: below normal
* 40% >= V > 35%: bad
* V > 40%: very badly

### Interest expense
(interest expense / operating income) * 100 % < 15 %: good
(interest expense / operating income) * 100 % < 23 %: normal
(interest expense / operating income) * 100 % < 30 %: below normal
(interest expense / operating income) * 100 % < 38 %: bad
(interest expense / operating income) * 100 % > 38 %: very bad

### Long term dept
x = long term debt / net income

x <= 4: good
4 < x <= 6: normal
6 < x <= 8: below normal
8 < x <= 10: bad
x > 10: very badly

### P/E and P/B
X - P/E
y - P/B

if xy > 10 or xy < 0.25: good
else if 10 >= xy > 8: normal
else: bad
