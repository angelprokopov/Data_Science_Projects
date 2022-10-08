import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
sns.set()
plt.style.use('fivethirtyeight')

data = pd.read_csv("AAPL.csv")
# print(data.head())

plt.figure(figsize=(10, 4))
plt.title("Apple Stock Prices")
plt.xlabel("Date")
plt.ylabel("Close")
plt.plot(data["Close"])
# plt.show()

print(data.corr())
sns.heatmap(data.corr())
plt.show()

x = data[["Open", "High", "Low"]]
y = data["Close"]
x = x.to_numpy()
y = y.to_numpy()
y = y.reshape(-1, 1)
xtrain, xtest, ytrain, ytest = train_test_split(x, y, train_size=0.2, random_state=42)
model = DecisionTreeRegressor()
model.fit(xtrain, ytrain)
ypred = model.predict(xtest)
data = pd.DataFrame(data={"Predicted Rate": ypred})
print(data.head())
