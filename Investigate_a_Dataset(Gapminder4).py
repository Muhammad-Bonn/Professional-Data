#!/usr/bin/env python
# coding: utf-8

# # Project: Investigate a Dataset - Gapminder World
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusion">Conclusion</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# ### Dataset Description 
# 
# **Gapminder** has collected a lot of information about how people live their lives in different countries, tracked across the years, and on a number of different indicators. For this project, we consider 4 different indicators to investigate which are (Life Expectancy Years, Total public health spending for person, Mean household income, Pump price for gasoline in USD per liter)
# 
# 
# ### Questions for Analysis
# With aiming to measure the Governments performance towards their people. We are going to investigate the Government's responsibility for public health and its effect on life expectancy years through first 2 datasets mentioned above, in addition to Government succeed in Economy section through measuring the percentage of income spending per person on gasoline by using the last 2 datasets mentioned above.

# In[2]:


# import statements for all of the packages that you plan to use.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


# Upgrade pandas to use dataframe.explode() function. 
get_ipython().system('pip install --upgrade pandas==0.25.0')


# ##  First Investigation: Public Health

# <a id='wrangling'></a>
# ## Data Wrangling

# > ### Load total_health_spending_per_person dataset file as health_spending

# In[30]:


health_spending = pd.read_csv('total_health_spending_per_person.csv')
health_spending.head()


# In[31]:


health_spending.info()


# > **So we have some columns with null values we need to clean**

# In[32]:


health_spending.shape


# > **We can notice that data for total health spending per person is only available from 1995 to 2010, So we will be restricted to this period in our investigation regarding public health**

# In[33]:


health_spending.describe()


# In[34]:


# seting 'country' column as the dataframe index
health_spending = health_spending.set_index('country')
health_spending.head(5)


# > ### Load Life_expectancy_years dataset file as lxy

# In[35]:


lxy = pd.read_csv('life_expectancy_years.csv')
lxy.head()


# In[36]:


lxy.shape


# In[37]:


lxy.info()


# In[38]:


# seting 'country' column as the dataframe index
lxy = lxy.set_index('country')
lxy.head(5)


# 
# ## Data Cleaning
#  

# > ### Cleaning Total health spending per person dataset

# In[39]:


# geting number of rows with null values
sum(health_spending.isnull().any(axis=1))
# as we have just 8 from 192 countries with null values we can neglect this countries data in our investigation


# In[40]:


health_spending = health_spending.dropna(how='any',axis=0)
sum(health_spending.isnull().any(axis=1))


# In[41]:


health_spending.head()


# In[42]:


# checking for duplicate values
sum(health_spending.duplicated())


# In[43]:


health_spending.columns


# In[44]:


# adding a new row with the World Average health spending data
health_spending.loc['World_Average'] = health_spending.mean(numeric_only = True)
health_spending.tail()


# > ### Cleaning Life expectancy years dataset

# In[45]:


# trimming dataset to include only data from 1995 to 2010 to be valid in comparison 
# with Total health spending per person dataset
years_to_investigate = list(health_spending.columns)
for x in lxy.columns :
    if x not in years_to_investigate:
        lxy.drop(columns=x, inplace = True)
lxy.head()


# In[46]:


# geting number of rows with null values
sum(lxy.isnull().any(axis=1))


# In[47]:


# checking for duplicate values
sum(lxy.duplicated())


# In[48]:


# adding a new row with the World Average Life expectancy years data
lxy.loc['World_Average'] = lxy.mean(numeric_only = True)
lxy.tail()


# > ### Removing countries that does not exist in both datasets
# 

# In[49]:


# removing countries that does not exist in both datasets
def Unity (df1,df2):
    countries_to_be_removed = [] # countries to be removed from both datasets
    for country in df1.index:
        if country not in df2.index:
            countries_to_be_removed.append(country)
    
    for country in df2.index:
        if country not in df1.index:
            countries_to_be_removed.append(country)
    
    for country in countries_to_be_removed:
        if country in df1.index:
            df1.drop(country,axis=0,inplace=True)
        elif country in df2.index:
            df2.drop(country,axis=0,inplace=True)
    return df1,df2


# In[50]:


Unity(lxy,health_spending);


# In[51]:


lxy.shape == health_spending.shape


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# > With other parameters are fixed we are going to investigate the effect of health spending on life expectancy through two ways, One by comparing the most spending countries and the lowest ones with their life expectancy over years to investigate if there is an effect of public health spending on life expectancy. The second way to investigate the increase percentage of life expectancy with increasing in health spending.
# 
# 
# ### Research Question 1 (First Way)

# In[52]:


# get the highest countries spending on public health
# by geting the average health spending for each country over the period from 1995 to 2010
health_spending['avg_spending'] = health_spending.mean(axis='columns')
highest_countries = health_spending['avg_spending'].nlargest(n=7)
highest_countries


# In[53]:


# geting the highest countries with life expectancy
# by geting the average life expectancy for each country over the period from 1995 to 2010
lxy['avg_years'] = lxy.mean(axis='columns')
highest_lxy = lxy['avg_years'].nlargest(n=7)
highest_lxy


# In[54]:


# geting how many countries from the highest health spedning countries with highest life expectancy
highest_lxy = lxy['avg_years'].nlargest(n=30)
highest_countries = health_spending['avg_spending'].nlargest(n=30)
i = 0
for country in highest_countries.index:
    if country in highest_lxy.index:
        i += 1
        print(i , country)


# > ### **Conclusion**: 
# From the result above we can find that there are 25 countries from the list of highest health spending countries in the first 30 countries list of highest life expectancy, supporting the assumption that there is a relation between spending on public health and life expectancy. NOTICING that United States, the highest country to spend on public health, is not in the 25 countries list we got, which could be an indicator to other parameters effect on life expectancy, and spending on public health is only one parameter we investigate here.
# 

# In[55]:


# get the lowest countries spending on public health
lowest_countries = health_spending['avg_spending'].nsmallest(n=7)
lowest_countries


# In[56]:


# geting the highest countries with life expectancy
lxy['avg_years'] = lxy.mean(axis='columns')
lowest_lxy = lxy['avg_years'].nsmallest(n=7)
lowest_lxy


# In[57]:


# geting how many countries from the lowest health spedning countries with lowest life expectancy
lowest_lxy = lxy['avg_years'].nsmallest(n=30)
lowest_countries = health_spending['avg_spending'].nsmallest(n=30)
i = 0
for country in lowest_countries.index:
    if country in lowest_lxy.index:
        i += 1
        print(i , country)


# > ### **Conclusion**:
# From the result above we can find that there are 17 countries from the list of lowest health spending countries in the last 30 countries list of lowest life expectancy.

# ### Research Question 2 (Ploting the realtion between health spedning versus life expectancy)

# In[58]:


# ploting the realtion between health spedning versus life expectancy
df1 = health_spending.iloc[:,[-1]]
df2 = lxy.iloc[:,[-1]]
df1.head(), df2.head()


# In[59]:


# merge 2 dataframes
df_to_plot = df1.merge(df2, left_on='country',right_on='country')
df_to_plot.head()


# In[62]:


# plot settings 
df_to_plot.plot.scatter(x = 'avg_spending', y ='avg_years', c= 'green', colormap='viridis')
plt.title('Data for Countries from 1995 to 2010', fontsize=25)
plt.xlabel('Average health spending per person in USD', fontsize=25)
plt.ylabel('Average life expectancy years in Years', fontsize=25)
plt.rcParams['figure.figsize'] = [25, 20]

# renames points on sactter plot by selecting only the highest and lowest countries in
# avg_spending and avg_years

for idx, row in  df_to_plot.iterrows():
    if idx in df_to_plot['avg_spending'].nlargest(3) or idx in df_to_plot['avg_years'].nlargest(3):
        plt.text(row['avg_spending'], row['avg_years'], idx, c = 'blue', fontsize=20)
    elif idx in df_to_plot['avg_spending'].nsmallest(3) or idx in df_to_plot['avg_years'].nsmallest(2):
        plt.text(row['avg_spending'], row['avg_years'], idx, c = 'red', fontsize=20)


# > For more fair comparison and clear investigation we are going to remove the highest 2 outliers in average health spending per person (United States , Luxembourg).

# In[63]:


# removing the highest 2 outliers
df_to_plot.drop(['United States','Luxembourg'],axis=0,inplace=True)
df_to_plot.shape


# In[65]:


# plot the realtion between health spedning versus life expectancy agin
# plot settings 
df_to_plot.plot.scatter(x = 'avg_spending', y ='avg_years', c= 'green', colormap='viridis')
plt.title('Data for Countries from 1995 to 2010', fontsize = 25)
plt.xlabel('Average health spending per person in USD', fontsize = 25)
plt.ylabel('Average life expectancy years in Years', fontsize = 25)
plt.rcParams['figure.figsize'] = [25, 20];

# renames points on sactter plot by selecting only the highest and lowest countries in
# avg_spending and avg_years

for idx, row in  df_to_plot.iterrows():
    if idx in df_to_plot['avg_spending'].nlargest(3) or idx in df_to_plot['avg_years'].nlargest(3):
        plt.text(row['avg_spending'], row['avg_years'], idx, c = 'blue', fontsize=20)
    elif idx in df_to_plot['avg_spending'].nsmallest(3) or idx in df_to_plot['avg_years'].nsmallest(2):
        plt.text(row['avg_spending'], row['avg_years'], idx, c = 'red', fontsize=20)
    elif idx == 'World_Average':
         plt.text(row['avg_spending'], row['avg_years'], idx, c = 'black', fontsize=20) 

sns.lmplot(x='avg_spending',y='avg_years',data=df_to_plot,fit_reg=True);


# > ## Conclusion: 
# from the second graph we can find a positive correlation between Average health spending per person and average life expectancy. 
# in general, in the first plot, the plot can be divided into 2 parts, the upper part from 70 to above 80 years on the vertical axis which include countries with high life expectancy a high spending on public health. The second part is the left part of the plot from 0 to 500 USD on the horizontal axis at which spending on public health almost has no related effect on life expectancy.

# ### Research Question 3  (The Second Way)

# > Investigate the increase in life expectancy percentage with increasing in public health spending

# In[66]:


# calculating change of public health spending over time for each country
health_spending_chane_rate = health_spending.drop(['avg_spending'],axis=1)
hscr = health_spending_chane_rate # for shorten
hscr = hscr.pct_change(axis='columns')
hscr['avg_spending_rate_%']= hscr.mean(axis='columns')*100
hscr['avg_spending_rate_%'].head()


# In[67]:


# calculating change of life expectancy over time for each country
lxy_change_rate = lxy.drop(['avg_years'],axis=1)
lxy_change_rate = lxy_change_rate.pct_change(axis='columns')
lxy_change_rate['avg_years_rate_%'] = lxy_change_rate.mean(axis='columns')*100
lxy_change_rate['avg_years_rate_%'].head()


# In[68]:


# merge the 2 dataframes health_spending_change_rate and life_expectancy_years_change_rate
df_1 = hscr.iloc[:,[-1]]
df_2 = lxy_change_rate.iloc[:,[-1]]
df_to_plot_2 = df_1.merge(df_2, left_on='country',right_on='country')
df_to_plot_2.head()


# In[69]:


plt.plot(df_to_plot_2,linestyle='solid')
plt.xticks(rotation=90)
plt.title('Health Spending Change_Rate VS Life Expectancy Years Change_Rate from 1995 to 2010',fontsize=25);


# In[70]:


# ploting df_to_plot_2 using lines is not the best way to illustrate relation between life expectancy and health spending
# so Let's try bar
df_to_plot_2.plot(kind='barh')
plt.rcParams['figure.figsize'] = [25, 25]
plt.title('Health Spending Change_Rate VS Life Expectancy Years Change_Rate from 1995 to 2010',fontsize=25);


# > ## Conclusion:
# With almost all countries increased their public health spending, their life expectancy also increased with different rates which depends on health spending but not along all the way which indicates that there are more parameters to investigate in this case and more inferential statistical analysis need to be done to get accurate and nondeceptive results.

# In[71]:


# get overall view using mean of the World_Average to investigate the realtion betwwen 
# average spending rate and average life expectancy years rate 
# also view egypt rates to compare with the world average
df_to_plot_2.loc['World_Average'], df_to_plot_2.loc['Egypt']


# In[72]:


x1,x2 = df_to_plot_2.loc['World_Average'].round(3)
res1 = 'The Global Average of Life Expectancy increased by'
res2 = 'in Spending on Public Health WorldWide over the period from 1995 to 2010'
print(('{} {} % with increase of {} % {}').format(res1,x2,x1,res2))


# # Second Investigation: The percentage of Income spending on Energy 

# ## Data Wrangling
# > ### Load mean_household_income per year dataset file as income

# In[73]:


income = pd.read_csv('mean_household_income.csv')
income.head()


# >* We have some cells with letter 'k' which indicates a thousand and will need to be modified

# In[74]:


income.info()


# >* and therefore there is some columns with int type and others with object type in the dataset

# In[77]:


income.describe()


# In[78]:


income.shape


# In[79]:


income.describe()


# >### Load pump_price_for_gasoline_us_per_liter dataset file as gasoline

# In[80]:


gasoline = pd.read_csv('pump_price_for_gasoline_us_per_liter.csv')
gasoline.head()


# In[81]:


gasoline.shape


# >* gasoline dataset has fewer data than income, so income will need to drop some columns and rows

# In[82]:


gasoline.describe()


# In[83]:


# gasoline.info() will be discussed in below


# ## Data Cleaning
# > ### Cleaning gasoline dataset

# In[84]:


# geting number of rows and columns with null values
sum(gasoline.isnull().any(axis=1)),sum(gasoline.isnull().any(axis=0)), gasoline.shape


# >* with null values in all rows and almost all columns, we can not neglect all null values at onec here.

# In[85]:


# get gasoline info
gasoline.info()


# >* it is obviuos here that the data for gasoline prices is available only for certain years, so we will drop years with 0 non-null values.

# In[86]:


# drop all empty columns
gasoline.dropna(how='all', axis=1, inplace=True)
gasoline.head()


# In[87]:


gasoline.info()


# In[88]:


# converting the type of last column to float
gasoline['2016'] = pd.to_numeric(gasoline['2016'], errors='coerce')


# In[89]:


gasoline.info()


# >* still the first 3 columns have not enough and less data than other columns, so we are going to drop them and the rest columns can be fill with mean of columns before and after that column i.e that year.

# In[90]:


# drop first 3 columns
gasoline.drop(columns=['1991','1992','1995'],axis=1,inplace=True)
gasoline.head()


# In[91]:


# investigate rows with null values
gasoline.isnull().sum(axis=1).value_counts()


# >* In gasoline dataset we have 10 columns with 10 values for every row. from above and with small number of rows with 6 null values or more (13 from 182 rows) we can remove this rows from gasoline dataset as it will be inaccurate to iterate over them to find the mean for filling null cells.

# In[92]:


# delete rows with 6 null values or more
for country_index in range(0,gasoline.shape[0],1):
    x = gasoline.loc[country_index].isnull().sum()
    if x >= 6:
        gasoline.drop([country_index], inplace = True )
gasoline.isnull().sum(axis=1).value_counts()


# In[94]:


gasoline.interpolate(method ='linear', axis = 0, inplace=True)
gasoline.isnull().sum(axis=1).value_counts()


# In[95]:


# remove the row with 2 null values which is the first row because there is 2 adjacent cells their data not available
gasoline.drop([0],inplace=True)
gasoline.isnull().sum(axis=1).value_counts()


# In[96]:


# checking for duplicate values
sum(gasoline.duplicated())


# In[97]:


gasoline.info()


# > ### Cleaning income dataset

# In[98]:


# include only years thats appears in gasoline prices dataset
income = income[gasoline.columns]


# In[99]:


# checking for duplicate values
sum(income.duplicated())


# In[101]:


# converting letter 'k' which indicates a thousand and converting year columns type to float
for year in income.columns[1:]:
    income.loc[:,year] = income.loc[:,year].replace({'K':'*1000', 'k':'*1000'}, regex = True).map(pd.eval).astype(float);


# In[102]:


income.head()


# In[103]:


income.info()


# In[104]:


# checking for null values in rows and columns with 
income.isnull().sum(axis=1).value_counts()


# > ### Removing countries that does not exist in both datasets
# 

# In[105]:


# seting 'country' column as the dataframe index for both datasets
income = income.set_index('country')
gasoline = gasoline.set_index('country')


# In[107]:


# removing countries that do not exist in both datasets
Unity(income,gasoline);


# In[108]:


gasoline.shape == income.shape, income.shape


# ## Exploratory Data Analysis
# 
# ### Research Question (Percentage of Income spent on gasoline yearly) (USD per person for 100 liter)

# In[109]:


gasoline.head()


# In[110]:


income.head()


# In[111]:


# Get percentage of Income spent on gasoline by divide gasoline dataset and income dataset 
# and multiply result dataframe by 100 liter to form percentage of Income spent per person on gasoline 
# in USD/100 Liter yearly.
data = pd.DataFrame(gasoline.values*100 / income.values, columns=gasoline.columns, index=gasoline.index)*100
data.head()


# In[112]:


# draw 1998 data
data['1998'].sort_values().plot(kind='barh');
plt.rcParams['figure.figsize'] = [25, 50];
plt.title('Percentage of yearly Income spent on gasoline for person per 100 liter % (1998)',fontsize=25);
plt.xlabel('Percentage of yearly Income spent on gasoline for person per 100 liter %',fontsize=25);
plt.ylabel('Countries',fontsize=40);


# In[113]:


# draw 2016 data
data['2016'].sort_values().plot(kind='barh');
plt.rcParams['figure.figsize'] = [25, 50];
plt.title('Percentage of yearly Income spent on gasoline for person per 100 liter % (2016)',fontsize=25);
plt.xlabel('Percentage of yearly Income spent on gasoline for person per 100 liter %',fontsize=25);
plt.ylabel('Countries',fontsize=40);


# >### **Conclusion**: 
# Compare Egypt percentage of Income spent on gasoline per person to the World average percentage.

# In[114]:


data.loc['World_Average'] = data.mean()
data.tail()


# In[115]:


data_to_plot = data.loc[['Egypt','World_Average']]
data_to_plot


# In[116]:


data_to_plot.T.plot(kind='bar', fontsize=25);
plt.title('Percentage of Income spent on gasoline for person per 100 liter %', fontsize=25);
plt.yticks(np.arange(0,6,0.1));


# <a id='conclusion'></a>
# 
# >## Conclusion:
# Generally, we can find a positive correlation between average health spending per person and average life expectancy supporting the assumption that there is a relation between spending on public health and life expectancy. Comparing Egypt percentage of Income spent on gasoline per person to the World average percentage results that Egyptian spend on gasoline less than the average of other People around the world. With almost all countries increased their public health spending, their life expectancy also increased with different rates depending on health spending but not along all the way which indicates that there are more parameters to investigate, and more inferential statistical analysis need to be done to get accurate and nondeceptive results.
# 
# 
# >## Limitations:
# Inferential Statistics needed to be done to investigate other parameters effect the Life Expectancy in first investigation beside spending on Public Health. Other limitations in the second investigate such as incomplete gasoline prices Dataset, also a Dataset for consumption in every country is needed for more accurate results and comparison.
# 
# 

# In[ ]:




