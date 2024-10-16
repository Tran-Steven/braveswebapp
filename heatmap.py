
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load the data from the specified Excel file
excel_file = "BattedBallData.xlsx"
xldata = pd.read_excel(excel_file,
                       sheet_name='Data',
                       usecols=['LAUNCH_ANGLE', 'EXIT_SPEED', 'EXIT_DIRECTION', 'HIT_DISTANCE', 'HANG_TIME', 'HIT_SPIN_RATE'])

# Compute the correlation matrix
correlation_matrix = xldata.corr()

# Display the correlation matrix as a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation Matrix')
plt.tight_layout()
plt.show()
