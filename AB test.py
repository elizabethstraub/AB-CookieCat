import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("C:\Projects - Coding\AB CookieCat\cookie_cats.csv")

print(df.head())

# EDA - verify number of unique users & how many in each group
print(df["userid"].nunique())
print(df.groupby("version")[["userid"]].nunique())

# EDA - do people install the game but never play it?
print(df[df["sum_gamerounds"] == 0]["userid"].count())

# EDA - What about 1-day rentention and 7-day retention?
df_retention = df[["retention_1","retention_7"]].mean()*100
print(f"1-day retention ratio: {round(df_retention[0],2)}% \
      \n7-days retention ratio: {round(df_retention[1],2)}%")

# EDA - Compare 1-day and 7-day retention for each AB group
df_retention_ab = df.groupby("version").agg({"userid":"count", "retention_1":"mean","retention_7":"mean", "sum_gamerounds":"sum"})
print(df_retention_ab)
# Result = Slight DECREASE in 1-day retention when the gate was moved to level 40 (44.2% vs 44.8%)
# Result = Significant DECREASE in 7-day rentention when the gate was moved to level 40 (18.2% vs 19.8%)

# Double-check results by bootstrapping with 500 samples
# Make a list with new 'bootstrapped' data
boot_1day = []
boot_7day = []
for i in range(500):
    boot_mean_1day = df.sample(frac=1, replace=True).groupby('version')['retention_1'].mean()
    boot_mean_7day = df.sample(frac=1, replace=True).groupby('version')['retention_7'].mean()
    boot_1day.append(boot_mean_1day)
    boot_7day.append(boot_mean_7day)

# Convert list into a dataframe
boot_1day = pd.DataFrame(boot_1day)
boot_7day = pd.DataFrame(boot_7day)

# Make a Kernel Density Estimate plot of the bootstrapped distributions
fig, (ax1,ax2) = plt.subplots(1, 2, sharey=True, figsize=(14,5))

boot_1day.plot.kde(ax=ax1)
ax1.set_xlabel("Retention rate",size=12)
ax1.set_ylabel("Number of samples",size=12)
ax1.set_title("Distribution of 1-day Retention Rate", fontweight="bold",size=15)

boot_7day.plot.kde(ax=ax2)
ax2.set_xlabel("Retention rate",size=12)
ax2.set_ylabel("Number of samples",size=12)
ax2.set_title("Distribution of 7-day Retention Rate", fontweight="bold",size=15)
plt.show()

# Result = demonstrates a slight difference between gate location

# Increase bootstrapped group size to 1000
boot_1day_v2 = []
boot_7day_v2 = []
for i in range(1000):
    boot_mean_1day_v2 = df.sample(frac=1, replace=True).groupby('version')['retention_1'].mean()
    boot_mean_7day_v2 = df.sample(frac=1, replace=True).groupby('version')['retention_7'].mean()
    boot_1day_v2.append(boot_mean_1day_v2)
    boot_7day_v2.append(boot_mean_7day_v2)

# Convert list into a dataframe
boot_1day_v2 = pd.DataFrame(boot_1day_v2)
boot_7day_v2 = pd.DataFrame(boot_7day_v2)

# Make a Kernel Density Estimate plot of the bootstrapped distributions
fig, (ax1,ax2) = plt.subplots(1, 2, sharey=True, figsize=(14,5))

boot_1day_v2.plot.kde(ax=ax1)
ax1.set_xlabel("Retention rate",size=12)
ax1.set_ylabel("Number of samples",size=12)
ax1.set_title("Distribution of 1-day Retention Rate \n with a larger sample", fontweight="bold",size=14)

boot_7day_v2.plot.kde(ax=ax2)
ax2.set_xlabel("Retention rate",size=12)
ax2.set_ylabel("Number of samples",size=12)
ax2.set_title("Distribution of 7-day Retention Rate \n with a larger sample", fontweight="bold",size=14)
plt.show()

# Result = still only demonstrates a slight difference between gate location

# Need to investigate further, add a colomn to demonstarte the percentage differance between groups
boot_1day['diff'] = ((boot_1day['gate_30'] - boot_1day['gate_40']) / boot_1day['gate_40'] * 100)
boot_7day['diff'] = ((boot_7day['gate_30'] - boot_7day['gate_40']) / boot_7day['gate_40'] * 100)

fig, (ax1) = plt.subplots(1, 1,figsize=(6,5))

boot_1day['diff'].plot.kde(ax=ax1, c="#ff99ff", label = "1-day retention")
boot_7day['diff'].plot.kde(ax=ax1, c= "#00bfff", label = "7-day retention")
ax1.set_xlabel("Difference (in %)",size=12)
ax1.set_ylabel("Density (in %)",size=12)
ax1.set_title("Difference in retention \n between A/B groups", fontweight="bold", size=14)
plt.legend()
plt.show()

# Result =  1- 2% difference  for 1- day retention.
# Result = 2 - 5% difference for for 7-day retention.

# What is the probability that retention is greater when gate is at level 30?
prob_1 = (boot_1day['diff']>0).sum()/len(boot_1day['diff'])
prob_7 = (boot_7day['diff']>0).sum()/len(boot_7day['diff'])

print(f"The probability that 1-day retention is greater when the gate is at level 30: {round(prob_1,2)*100}% \
      \nThe probability that 7-days retention is greater when the gate is at level 30: {(prob_7)*100}% ")

# - End result -
# 99.8% probability that 7-day retention is higher when the gate is at level 30 than when it is at level 40.
# 95 % probability that 1-day retention is higher when the gate is at level 30 than when it is at level 40.

# Conclusion - The current gate location results in higher player rentention. To optimize both 1 and 7-day rentention, we should not move the gate from level 30 to level 40.

