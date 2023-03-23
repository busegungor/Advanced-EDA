# requirements
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def import_csv(dataframe):
    df = pd.read_csv(dataframe)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 500)
    pd.set_option('display.html.table_schema', True)
    return df
df = import_csv("/Users/busegungor/Desktop/ds.salaries.csv")

# 1. Genel Resim
def check_df(dataframe):
    print("#### Shape ####")
    print(dataframe.shape)
    print("#### Columns ####")
    print(dataframe.columns)
    print("#### Types ####")
    print(dataframe.dtypes)
    print("#### NA ####")
    print(dataframe.isnull().sum())
    print("#### Quantiles ####")
    print(dataframe.describe([0, 0.05, 0.95, 0.99, 1]))
check_df(df)

# 2. Analysis of Categorical Variables


category_column = [col for col in df.columns if str(df[col].dtypes) in ["object", "category", "bool"]]
number_but_category = [col for col in df.columns if df[col].nunique() < 10 and df[col].dtypes in ["int", "float"]]
category_but_cardinality = [col for col in df.columns if df[col].nunique() > 20 and str(df[col].dtypes) in ["category", "object"]]
category_column = category_column + number_but_category
category_column = [col for col in category_column if col not in category_but_cardinality]

def category_summary(dataframe, col_name, plot=False):
    print(pd.DataFrame({col_name: dataframe[col_name].value_counts(),
                        "Ratio": 100 * dataframe[col_name].value_counts() / len(dataframe)}))
    print("###########################")
    if plot:
        sns.countplot(x=dataframe[col_name], data=dataframe)
        plt.show(block=True)

for col in category_column:
    if df[col].dtypes == "bool":
        df[col] = df[col].astype(int)
        category_summary(df, col, plot=True)
    else:
        category_summary(df, col, plot=True)

# 3. Analysis of Numerical Variables

number_columns = [col for col in df.columns if df[col].dtypes in ["int", "float"]]
number_columns = [col for col in number_columns if col not in category_column]

def number_summary(dataframe, numberical_col, plot=False):
    quantiles = [0, 0.05, 0.95, 0.99, 1]
    print(dataframe[numberical_col].describe(quantiles).T)
    if plot:
        dataframe[numberical_col].hist()
        plt.xlabel(numberical_col)
        plt.title(numberical_col)
        plt.show(block=True)

for col in number_columns:
    number_summary(df, col, plot=True)

# 4. Analysis of Target Variable

# Hedef değişkenin kategorik değişkenler ile analizi
def target_summary_with_cat(dataframe, target, categorical_col):
    print(pd.DataFrame({"Target_Mean": dataframe.groupby(categorical_col)[target].mean()}))

for col in category_column:
    target_summary_with_cat(df, "salary", col)

# Hedef değişkenin sayısal değişkenler ile analizi
def target_summary_with_num(dataframe, target, numerical_col):
    print(dataframe.groupby(target).agg({numerical_col: "mean"}))

for col in number_columns:
    target_summary_with_num(df, "salary", col)

# 5. Analysis of Correlation

number_col = [col for col in df.columns if df[col].dtypes in ["int", "float"]]
corr = df[number_col].corr()
sns.set(rc={'figure.figsize': (12, 12)})
sns.heatmap(corr, cmap="RdBu")
plt.show()

# Yüksek Korelasyonlu Değişkenlerin Silinmesi

cor_matrix = df.corr().abs()
upper_triangle_matrix = cor_matrix.where(np.triu(np.ones(cor_matrix.shape), k=1).astype(np.bool))
drop_list = [col for col in upper_triangle_matrix.columns if any(upper_triangle_matrix[col] > 0.90)]
df.drop(drop_list, axis=1)

def high_correlated_columns(dataframe, plot=False, corr_th=0.90):
    corr = dataframe.corr()
    cor_matrix = corr.abs()
    upper_triangle_matrix = cor_matrix.where(np.triu(np.ones(cor_matrix.shape), k=1).astype(np.bool))
    drop_list = [col for col in upper_triangle_matrix.columns if any(upper_triangle_matrix[col] > 0.90)]
    if plot:
        sns.set(rc={'figure.figsize': (12, 12)})
        sns.heatmap(corr, cmap="RdBu")
        plt.show()
    return drop_list

high_correlated_columns(df)
drop_list = high_correlated_columns(df, plot=True)
df.drop(drop_list, axis=1)
high_correlated_columns(df.drop(drop_list, axis=1), plot=True)










