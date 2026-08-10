import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from pathlib import Path

## File import und creating a results folder
folder = Path(__file__).resolve().parent
results_folder = folder / "results"
results_folder.mkdir(exist_ok=True)

Spot_prices = pd.read_excel(folder / "Gro_handelspreise_202512010000_202601010000_Viertelstunde.xlsx", skiprows=9)
reBAP_prices = pd.read_excel(folder / "REBAP_2025_12.xlsx", skiprows=4)

## Parameters
BATTERY_CAPACITY= 0.1 #MWh
STRESS_PERCENTILE = 0.95 
ROLLING_WINDOW = 8 # to calculate spot price volatility 

## Exploratory Data Analysis
def inspect_dataframe(df, name):
    print(f"\n{name}")
    print("-"*40)
    print(df.shape)
    print(df.dtypes)
    print(df.head())
    print(df.columns)
    print("nan werte", df.isnull().sum().sum())

inspect_dataframe(Spot_prices, "Spotpreise")
inspect_dataframe(reBAP_prices, "reBAP")

###############################################################################################
#############################################################################################
## Creating a new dataframe to keep only necessary data
# Convert to datetime
Spot_prices["Datum von"] = pd.to_datetime(Spot_prices["Datum von"], dayfirst=True)
reBAP_prices["Datum Uhrzeit von"] = pd.to_datetime(reBAP_prices["Datum Uhrzeit von"], dayfirst=True)

# copy relevant data to new dataframes
spot = Spot_prices[["Datum von", "Deutschland/Luxemburg [€/MWh]"]].copy()
rebap = reBAP_prices[["Datum Uhrzeit von", "reBAP _pos\n(EUR/MWh)"]].copy()

# rename columns for simplicity
spot.columns = ["timestamp", "spot_preis"]
rebap.columns = ["timestamp", "rebap"]

# new Dataframe
df = pd.merge(
    spot,
    rebap,
    on="timestamp",
    how="inner"
)

inspect_dataframe(df,"Merged_df") #investigating the dataframe 
df['spread']= df["rebap"]-df['spot_preis'] #creating a new column to calculate spread

#creating a new column for spot price volatility on a 2 hour rolling basis
df["spot_volatilität"] = (df["spot_preis"].rolling(window=8).std()) 

##############################################################################################
###########################################################################################

# A new data frame to identify stressful quarterly hours. Stress events are those with the top 5% spread
df_stress_events=  df[df['spread'].abs() >= df['spread'].abs().quantile(STRESS_PERCENTILE)]
df_stress_events = df_stress_events.copy()  # avoids a SettingWithCopyWarning below
df_stress_events["hour"] = df_stress_events["timestamp"].dt.hour
inspect_dataframe(df_stress_events, "Stress events")

###############################################################################################
################################################################################################

# Calculating savings from control measures in effect only in the event of stress events
df_stress_events['ersparnisse']= BATTERY_CAPACITY*df_stress_events['spread'].abs()
total_savings_stress_events= df_stress_events['ersparnisse'].sum()
savings_stress_pro_volume= total_savings_stress_events/ (BATTERY_CAPACITY*len(df_stress_events))
print(f"Ersparnisse bei Steuerungsmaßnahmen in Stress events: {total_savings_stress_events:.2f} Euro")
print(f"Ersparnisse pro MWh bei Steuerungsmaßnahmen in Stress events: {savings_stress_pro_volume:.2f} €/MWh")


# Calculation of savings achieved through control measures when the Battery is available always 
df['ersparnisse wenn immer']= BATTERY_CAPACITY*df['spread'].abs()
total_savings_always= df['ersparnisse wenn immer'].sum()
savings_pro_volume= total_savings_always/ (BATTERY_CAPACITY*len(df))
print(f"Ersparnisse bei Steuerungsmaßnahmen wenn Batterie immer verfügbar: {total_savings_always:.2f} Euro")
print(f"Ersparnisse pro MWh bei Steuerungsmaßnahmen wenn Batterie immer verfügbar: {savings_pro_volume:.2f} €/MWh")

#  Percentage of costs covered through targeted use
share_captured = total_savings_stress_events / total_savings_always
share_of_time = len(df_stress_events) / len(df)
print(f"Gezielter Einsatz erfasst {share_captured:.1%} der theoretisch möglichen Gesamteinsparung,")
print(f"bei nur {share_of_time:.1%} der Einsatzzeit")



## Correlation calculation
 ## Spot price and rebap
corr_matrix = df[["spot_preis", "rebap"]].corr() ## matrix als output
print(corr_matrix.round(2))

 ##Spot price volatility and reBAP
corr = df["spot_volatilität"].corr(df["rebap"]) #pearson coefficient as default
print(f"Korrelation zwischen Spotpreis Volatilität und reBAP: {corr:.2f}")

threshold = df["spot_volatilität"].abs().quantile(0.75)

high_vol = df[df["spot_volatilität"] >= threshold]
low_vol = df[df["spot_volatilität"] < threshold]

print (f"Durchschnittlicher reBAP (hohe Volatilität):{high_vol["rebap"].abs().mean():.2f}")
print(f"Durchschnittlicher reBAP (geringe Volatilität): {low_vol["rebap"].abs().mean():.2f}")

#############################################Plotting#########################################
################################################################################################
# Plot 1 - correlation matrix
plt.figure(figsize=(5,5))

sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="coolwarm",
    square=True,
    vmin=-1,
    vmax=1
)
plt.title("Korrelationsmatrix")
plt.savefig(results_folder / "plot1_korrelationsmatrix.png", dpi=150, bbox_inches="tight")

# Plot 2 - scatterplot
plt.figure(figsize=(8,6))

sns.scatterplot(
    data=df,
    x="spot_preis",
    y="rebap",
    alpha=0.6
)
plt.xlabel("Spotpreis [€/MWh]")
plt.ylabel("reBAP [€/MWh]")
plt.title("Spotpreis vs. reBAP")

plt.tight_layout()
plt.savefig(results_folder / "plot2_scatterplot.png", dpi=150, bbox_inches="tight")


# Plot 3 - time series graph
plt.figure(figsize=(15,5))

plt.plot(df["timestamp"], df["spot_preis"], label="Spot")
plt.plot(df["timestamp"], df["rebap"], label="reBAP")

plt.xlabel("Zeit")
plt.ylabel("€/MWh")
plt.title("Spotpreis und reBAP über Zeit")

plt.legend()
plt.tight_layout()
plt.savefig(results_folder / "plot3_timeseries.png", dpi=150, bbox_inches="tight")

# Plot 4 - Frequency of stress events by time of day
plt.figure(figsize=(10,5))

sns.countplot(data=df_stress_events, x="hour", color="steelblue")

plt.xlabel("Stunde des Tages")
plt.ylabel("Anzahl Stress-Ereignisse")
plt.title("Häufigkeit von Stress-Ereignissen nach Tageszeit")

plt.tight_layout()
plt.savefig(results_folder/ "plot4_haeufigkeitstressevents.png", dpi=150, bbox_inches="tight")

plt.show() # einmal ganz am Ende, da es den Code pausiert und wartet darauf, dass das Bild geschlossen wird, wenn es nach
## jeder Bild Herstellung geschrieben ist