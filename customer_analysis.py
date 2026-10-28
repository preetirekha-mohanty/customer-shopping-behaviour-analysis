import pandas as pd

#1.Load the dataset
df=pd.read_csv(r'D:\Customer Shopping Behaviour Analysis\customer_shopping_behaviour.csv')

#2. Display the first five rows
print(df.head(5))

#3. Display Dataset information 
print(df.info())


# 4. Display summary statistics
print(df.describe(include="all"))

# 5. Check missing values
print(df.isnull().sum())

# 6. Fill missing review ratings using the median rating for each product category
df["Review Rating"] = df.groupby("Category")[
    "Review Rating"
].transform(lambda x: x.fillna(x.median()))

# 7. Standardize column names
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(" ", "_")
df = df.rename(
    columns={"purchase_amount_(usd)": "purchase_amount"}
)

# 8. Create customer age groups
labels = ["Young Adult", "Adult", "Middle-aged", "Senior"]
df["age_group"] = pd.qcut(
    df["age"], q=4, labels=labels
)

# 9. Convert purchase frequency into days
frequency_mapping = {
    "Fortnightly": 14,
    "Weekly": 7,
    "Monthly": 30,
    "Quarterly": 90,
    "Bi-Weekly": 14,
    "Annually": 365,
    "Every 3 Months": 90
}

df["purchase_frequency_days"] = (
    df["frequency_of_purchases"].map(frequency_mapping)
)

# 10. Check discount and promo code consistency
print("\nDiscount and promo code match:")
print(
    (df["discount_applied"] == df["promo_code_used"]).all()
)

# 11. Drop the redundant promo code column
df = df.drop(columns=["promo_code_used"])

# 12. Check cleaned data
print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nCleaned data preview:")
print(df.head())

# 13. Save the cleaned dataset
df.to_csv("customer_shopping_behaviour_cleaned.csv", index=False)

print("\nData cleaning completed successfully!")

from sqlalchemy import create_engine

# MySQL connection
username = "root"
password = "YOUR PASSWORD"
host = "localhost"
port = "3306"
database = "customer_behavior"

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")

# Write DataFrame to MySQL
table_name = "customer"   # choose any table name
df.to_sql(table_name, engine, if_exists="replace", index=False)

# Read back sample
pd.read_sql("SELECT * FROM customer LIMIT 5;", engine)