# Finance-Calculator
Langauge: [[Python]]
# Purposes
In general I want to take data from yahoo finance using an [[API]]. I will then use that information to have useful tools and mathematical functions that would be important to anyone in finance.

---
# Knowledge Exhibited
- [[Excel file conversion]] and export
- Easily create charts
- Pull data with [[API]]
- Solve mathematical equations

---
# Steps
1. Import yfinance as the API
	1. Alternatively find the best free API for stocks
2. Use data parsing and storage to show data in as a table or [[dataframe]]
3. Take data ask for intervals and stocks
4. Transform data into charts
5. Transform data into mathmatical equations
	1. Think of adding features such as the top 10 equations you would need in finance
	2. Create a LBO or DCF model within python
	3. Black Scholes Model
6. Transform data into charts to view
7. Call more than one stock to do comparisons
8. Export option for excel
9. Display data in a more beautiful way (ie styling features would be cool)

---
# API
[[Financial API]] are going to help me take data from several sources and then I can learn to do stuff with it. 

---
# Graph
The library we will use for graphing is as follows:
- [[Matplotlib]]
- [[Pandas]]

---
# DCF
- https://www.youtube.com/watch?v=yIJjUzyNGqg&ab_channel=Dividendology

# Learning Process
1. API
	1. API are sometimes annoying to use
	2. API library has several tools that you can use
2. Issues with [[yfinance]]
	1. Sometimes the financial statements are treated as a dataframe (rows, columns) however, sometimes they need to be [[transposed]]. Transposing is basically turning it into row and column system so you can parse the numbers you need
3. [[Matplotlib]]
	1. Super useful to data analysis with and can be done using x,y axis and plt.action to do different stuff with graphs
4. Creating exits and checks
	1. I have ot create exit points fpr the code
	2. I have to add y,n inputs that can take both "Y" and "y"
5. Code formatting
	1. I should go back and format the code better
6. I need to create a buy or sell option for the stocks
7. Create a LOOP that allows to run the program
8. Create a UI thats better
9. Create a better intro that explains what the program does 
