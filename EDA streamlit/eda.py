import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter

import matplotlib.pyplot as plt
import pandas_bokeh
import missingno


plt.style.use ("default")
#logic to Separate Continuous & Categorical Columns 
def find_cat_cont_cols(df): 
    cont_cols,cat_cols = [],[]
    for col in df.columns:
        if len(df[col].unique())<= 25 or df[col].dtype == np.object_:  # if less than 25 unique values
            cat_cols.append(col.strip())
        else:
            cont_cols.append(col.strip())
    return cont_cols , cat_cols

# Create Correlation Chart using matplotlib 
def create_correlation_chart(corr_df):
    fig = plt.figure(figsize=(15,15))
    plt.imshow(corr_df.values, cmap="Blues")
    plt.xticks(range(corr_df.shape[0]), corr_df.columns, rotation =90, fontsize =15)
    plt.yticks(range(corr_df.shape[0]), corr_df.columns, fontsize =15)
    plt.colorbar()
    
    for i in range(corr_df.shape[0]):
        for j in range(corr_df.shape[0]):
            plt.text(i,j, "{:.2f}".format(corr_df.values[i,j]), color ="red", ha= "center", fontsize= 14, fontweight= "bold")
    
    return fig 

def create_missing_values_bar(df):
    missing_fig = plt.figure(figsize = (10,5))
    ax = missing_fig.add_subplot(111)
    missingno.bar(df, figsize= (10,5), fontsize= 12, ax= ax)
    
    return missing_fig

# Web app / Dashboard code 
st.set_page_config(page_icon=":bar_chart:" , page_title= "EDA")
st.title("EDA Automation")
st.caption("Upload CSV file to see various Charts related to EDA. Please upload file that has both continuous columns and categorical columns. Once you upload file, various charts, widgets and basic stats will be displayed. As a sample example, you can upload famous <a href='https://www.kaggle.com/competitions/titanic/data?select=train.csv'>Titanic Dataset</a> available from Kaggle.", unsafe_allow_html=True)
upload = st.file_uploader(label= "Upload File Here " , type = "csv")

if upload:
    df = pd.read_csv(upload)  # reaading the file
    
    tab1, tab2, tab3 = st.tabs(["Dataset Overview :clipboard:", "Individual Column Stats :bar_chart:", "Explore Relation Features :chart:"])
    
    with tab1:  #Dataset Overview
        st.subheader("1. Dataset")
        st.write(df)
        
        cont_cols, cat_cols = find_cat_cont_cols(df)
        
        st.subheader("2. Dataset Overview")
        st.markdown("<span style='font-weight:bold;'>{}</span> : {}".format("Rows", df.shape[0]), unsafe_allow_html= True)
        st.markdown("<span style='font-weight:bold;'>{}</span> : {}".format("Duplicates", df.shape[0]-df.drop_duplicates().shape[0]), unsafe_allow_html= True)
        st.markdown("<span style='font-weight:bold;'>{}</span> : {}".format("Features", df.shape[1]), unsafe_allow_html= True)
        st.markdown("<span style='font-weight:bold;'>{}</span> : {}".format("Categorial Columns", len(cat_cols)), unsafe_allow_html= True)
        st.write(cat_cols)
        st.markdown("<span style='font-weight:bold;'>{}</span> : {}".format("Continuous Columns", len(cont_cols)), unsafe_allow_html= True)
        st.write(cont_cols)
        
        corr_df = df[cont_cols].corr()
        corr_fig = create_correlation_chart(corr_df)
        
        st.subheader("3. Correlation Chart")
        st.pyplot(corr_fig, use_container_width=True)
        
        st.subheader("4. Missing Values Distribution")
        missing_fig = create_missing_values_bar(df)
        st.pyplot(missing_fig, use_container_width= True)

    with tab2:  #Individual Column Stats
        df_descr = df.describe()
        st.subheader("Analyze Individual Feature Distribution")
        
        st.markdown("#### 1. Understand Continuous Feature")
        feature = st.selectbox(label= "Select Continuous Feature", options= cont_cols, index=0)
        
        na_cnt = df[feature].isna().sum()
        st.markdown("<span style='font-weight:bold;'>{}</span> : {}".format("Count", df_descr[feature]['count']), unsafe_allow_html= True)
        st.markdown("<span style='font-weight:bold;'>{}</span> : {} / ({:.2f}%)".format("Missing Count",na_cnt, na_cnt/df.shape[0]*100), unsafe_allow_html= True)
        st.markdown("<span style='font-weight:bold;'>{}</span> : {:.2f}".format("Mean", df_descr[feature]['mean']), unsafe_allow_html= True)
        st.markdown("<span style='font-weight:bold;'>{}</span> : {:.2f}".format("Standard Deviation", df_descr[feature]['std']), unsafe_allow_html= True)
        st.markdown("<span style='font-weight:bold;'>{}</span> : {}".format("Minimum", df_descr[feature]['min']), unsafe_allow_html= True)
        st.markdown("<span style='font-weight:bold;'>{}</span> : {}".format("Maximum", df_descr[feature]['max']), unsafe_allow_html= True)
        st.markdown("<span style='font-weight:bold;'>{}</span> : ".format("Quantiles"), unsafe_allow_html= True)
        st.write(df_descr[[feature]].T[['25%', '50%','75%']])
        #Histogram
        hist_fig= df.plot_bokeh.hist(y= feature, bins=50, legend= False, vertical_xlabel= True, show_figure= False)
        st.bokeh_chart(hist_fig, use_container_width= True)
        
        st.markdown("#### 2. Understand Categorical Feature")
        feature_cat= st.selectbox(label= "Select Categorical Feature", options= cat_cols, index=0)
        #categorical columns destribution
        cnts = Counter(df[feature_cat].values)
        df_cnts= pd.DataFrame({"Type": cnts.keys(), "Values" : cnts.values()})
        bar_fig= df_cnts.plot_bokeh.bar(x="Type", y="Values",color= "tomato", legend= False, vertical_xlabel= True, show_figure= False)
        st.bokeh_chart(bar_fig,use_container_width= True)

    with tab3:  #Explore Relation Features
        st.subheader("Explore Relation Between Features of Dataset")
        col1,col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox(label= "X-Axis", options= cont_cols,index=0)
        with col2:
            y_axis = st.selectbox(label= "Y-Axis", options= cont_cols, index=1)
        
        color_encode= st.selectbox(label= "Color-Encode", options=[None,]+cat_cols)
        
        scatter_fig= df.plot_bokeh.scatter(
                                        x= x_axis, y= y_axis, category= color_encode if color_encode else None,
                                        title= "{} VS {}".format(x_axis.capitalize(), y_axis.capitalize()),
                                        figsize= (600,500), fontsize_title= 20, fontsize_label=15,
                                        show_figure=False
                                        )
        st.bokeh_chart(scatter_fig,use_container_width= True)
        