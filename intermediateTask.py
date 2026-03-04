import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os

warnings.filterwarnings('ignore')

# =========================
# CHECK CURRENT DIRECTORY
# =========================

print("Current Folder:", os.getcwd())
print("Files in Folder:", os.listdir())

# =========================
# LOAD DATA
# =========================

print("\nLoading data...")

try:
    df = pd.read_csv("store_data.csv", encoding="latin1")
    
    print(f"\n✅ Data loaded successfully!")
    print(f"Rows: {df.shape[0]}  Columns: {df.shape[1]}")
    
    print("\nFirst 5 rows:")
    print(df.head())

except Exception as e:
    print("\n❌ Error while loading CSV file")
    print("Error:", e)
    exit()

# =========================
# CLEAN DATA
# =========================

print("\n🧹 Cleaning data...")

numeric_cols = ['Sales', 'Profit', 'Quantity', 'Discount']

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

df.dropna(subset=[col for col in numeric_cols if col in df.columns], inplace=True)

print("Cleaned dataset shape:", df.shape)

# =========================
# ANALYSIS
# =========================

print("\n📊 GENERATING INSIGHTS...")

# -------------------------
# SALES & PROFIT BY CATEGORY
# -------------------------

if 'Category' in df.columns and 'Sales' in df.columns:

    cat_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
    cat_profit = df.groupby('Category')['Profit'].sum().sort_values(ascending=False)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,5))

    cat_sales.plot(kind='bar', ax=ax1, color='skyblue')
    ax1.set_title("Total Sales by Category")
    ax1.tick_params(axis='x', rotation=45)

    cat_profit.plot(kind='bar', ax=ax2, color='lightgreen')
    ax2.set_title("Total Profit by Category")
    ax2.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig("category_analysis.png")
    plt.show()

# -------------------------
# PROFIT MARGIN
# -------------------------

if 'Profit' in df.columns and 'Sales' in df.columns:

    df['Profit_Margin'] = (df['Profit'] / df['Sales']) * 100

    print("\n💰 Average Profit Margin:", round(df['Profit_Margin'].mean(),2), "%")

    margin_by_cat = df.groupby('Category')['Profit_Margin'].mean().sort_values(ascending=False)

    print("\nProfit Margin by Category:")
    print(margin_by_cat)

# -------------------------
# TOP PRODUCTS
# -------------------------

if 'Product Name' in df.columns:

    top_products = df.groupby('Product Name')['Sales'].sum().nlargest(10)

    plt.figure(figsize=(10,6))
    top_products.plot(kind='barh')

    plt.title("Top 10 Products by Sales")

    plt.tight_layout()
    plt.savefig("top_products.png")
    plt.show()

# -------------------------
# CORRELATION HEATMAP
# -------------------------

num_cols = ['Sales','Profit','Quantity','Discount']

available = [col for col in num_cols if col in df.columns]

if len(available) > 1:

    corr = df[available].corr()

    plt.figure(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)

    plt.title("Sales Factors Correlation")

    plt.savefig("correlation.png")
    plt.show()

# =========================
# BUSINESS INSIGHTS
# =========================

print("\n🎯 KEY RECOMMENDATIONS:")

if 'Category' in df.columns:
    print("1. Focus on:", df.groupby('Category')['Profit'].sum().idxmax(), "- highest profit")

if 'Sub-Category' in df.columns:
    print("2. Fix negative profit in:", df[df['Profit'] < 0]['Sub-Category'].value_counts().index[0])

if 'Product Name' in df.columns:
    print("3. Push top product:", df.groupby('Product Name')['Sales'].sum().idxmax())

print("\n✅ Analysis complete!")
print("Charts saved as PNG files.")