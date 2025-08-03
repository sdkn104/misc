from sklearn.datasets import fetch_california_housing
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load California housing dataset
data = fetch_california_housing()

# Create dataframe
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target

# Display basic statistics
print(df.describe())

# Visualize data
sns.pairplot(df)
plt.show()
