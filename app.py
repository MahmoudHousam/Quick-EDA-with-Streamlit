import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import codecs
import streamlit.components.v1 as components
import sweetviz as sv
import helpers as hp

st.set_option("deprecation.showfileUploaderEncoding", False)

st.title("Quick EDA")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding="utf-8")
    st.write(df.head(10))


if st.checkbox("EDA"):
    hp.explore_nans(df, "Column NaNs")
    # st.plotly_chart(
    #     go.Figure(
    #         go.Table(
    #             header=dict(
    #                 values=df.dtypes.reset_index().columns.tolist(), align="left"
    #             ),
    #             cells=dict(
    #                 values=df.dtypes.reset_index().transpose().values.tolist(),
    #                 align="left",
    #             ),
    #         )
    #     )
    # )
    st.plotly_chart(
        go.Figure(
            go.Table(
                header=dict(
                    values=df.describe().reset_index().columns.tolist(), align="left"
                ),
                cells=dict(
                    values=df.describe().reset_index().transpose().values.tolist(),
                    align="left",
                ),
            ),
            go.Layout(title="Dataframe Summary"),
        )
    )
    st.write(
        "Dataframe shape:",
        "number of rows and columns are {}, {} respectively".format(
            df.shape[0], df.shape[1]
        ),
    )


if st.checkbox("Select Columns to show"):
    df_columns = df.columns.tolist()
    selected_columns = st.multiselect("Select", df_columns)
    new_df = df[selected_columns].head(10)
    st.dataframe(new_df)

st.subheader("Data Visualization")

df_columns = df.columns.tolist()
selected_column = st.selectbox("select column", df_columns)
plot_type = st.selectbox("Select a chart type", ["Pie", "Bar", "Line", "Boxplot"])


if st.button("Generate Plot"):
    if selected_column:
        if plot_type == "Pie":
            count = df[selected_column].value_counts()
            data = [go.Pie(labels=count.index.tolist(), values=count.values.tolist())]
            layout = go.Layout(title="{}".format(selected_column))
            fig = go.Figure(data=data, layout=layout)
            st.plotly_chart(fig, use_container_width=True)
        elif plot_type == "Bar":
            count = df[selected_column].value_counts()
            data = [go.Bar(x=count.index.tolist(), y=count.values.tolist())]
            layout = go.Layout(
                title="{}".format(selected_column),
                xaxis=dict(showgrid=False, rangemode="tozero"),
                yaxis=dict(showgrid=False, rangemode="tozero"),
            )
            fig = go.Figure(data=data, layout=layout)
            st.plotly_chart(fig, use_container_width=True)
        elif plot_type == "Boxplot":
            data = [go.Box(y=df[selected_column].tolist(), name=selected_column)]
            layout = go.Layout(
                title="{}".format(selected_column),
                xaxis=dict(showgrid=False, rangemode="tozero"),
                yaxis=dict(showgrid=False, rangemode="tozero"),
            )
            fig = go.Figure(data=data, layout=layout)
            st.plotly_chart(fig, use_container_width=True)
        elif plot_type == "Line":
            count = df[selected_column].value_counts()
            data = [go.Scatter(x=count.index.tolist(), y=count.values.tolist())]
            layout = go.Layout(
                title="{}".format(selected_column),
                xaxis=dict(showgrid=False, rangemode="tozero"),
                yaxis=dict(showgrid=False, rangemode="tozero"),
            )
            fig = go.Figure(data=data, layout=layout)
            st.plotly_chart(fig, use_container_width=True)

# st.subheader("Explore with Sweetviz")

# def st_sweetviz_display(html_report, width=1000, height=500):
# 	report = codecs.open(html_report, 'r')
# 	read_file = report.read()
# 	return components.html(read_file, width=width, height=height, scrolling=True)

# if st.button("Generate EDA Report"):
# 	report = sv.analyze(df)
# 	report.show_html()
# 	st_sweetviz_display("SWEETVIZ_REPORT.html")