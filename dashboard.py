import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

#titulo pestaña
st.set_page_config(page_title="intervencionismo", page_icon=":bar_chart:",layout="wide")

#titulo pagina
st.title(" :bar_chart: Radiologia Vascular e Intervencionista")

#archivo load
fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_excel(filename)
else:
    os.chdir(r"C:\Users\crisa\Documents\Agustindoc\Streamlit")
    df = pd.read_excel("data.xlsx")

# Crear columnas en Streamlit
col1, col2 = st.columns((2))
df["fecha"] = pd.to_datetime(df["fecha"])

# Getting the min and max date 
startDate = pd.to_datetime(df["fecha"]).min()
endDate = pd.to_datetime(df["fecha"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["fecha"] >= date1) & (df["fecha"] <= date2)].copy()

# Barra de filtros
st.sidebar.header("Filtros: ")

# Filtro operador
operador = st.sidebar.multiselect("Operador", df["operador"].unique())
if not operador:
    df2 = df.copy()
else:
    df2 = df[df["operador"].isin(operador)]

# Filtro metodo
metodo = st.sidebar.multiselect("Metodo", df2["metodo"].unique())
if not metodo:
    df3 = df2.copy()
else:
    df3 = df2[df2["metodo"].isin(metodo)]

# Filtro procedimiento
procedimiento = st.sidebar.multiselect("Procedimiento", df3["procedimiento"].unique())
if not procedimiento:
    df4 = df3.copy()
else:
    df4 = df3[df3["procedimiento"].isin(procedimiento)]

# Filtro obra social
os = st.sidebar.multiselect("Obra Social", df4["os"].unique())
if not os:
    df5 = df4.copy()
else:
    df5 = df4[df4["os"].isin(os)]

# Filtro complicaciones
complicaciones = st.sidebar.multiselect("Complicaciones", df5["complicaciones"].unique())
if not complicaciones:
    filtered_df = df5.copy()
else:
    filtered_df = df5[df5["complicaciones"].isin(complicaciones)]

# Filtros por operador, metodo, procedimiento, obra social y complicaciones

if not operador and not metodo and not procedimiento and not os and not complicaciones:
    filtered_df = df
elif not operador and not metodo and not procedimiento and not os:
    filtered_df = df[df["complicaciones"].isin(complicaciones)]
elif not operador and not metodo and not procedimiento and not complicaciones:
    filtered_df = df[df["os"].isin(os)]
elif not operador and not metodo and not procedimiento:
    filtered_df = df[df["os"].isin(os) & df["complicaciones"].isin(complicaciones)]
elif not metodo and not procedimiento and not os:
    filtered_df = df[df["operador"].isin(operador)]
elif not metodo and not procedimiento and not complicaciones:
    filtered_df = df[df["operador"].isin(operador) & df["os"].isin(os)]
elif not metodo and not procedimiento:
    filtered_df = df[df["operador"].isin(operador) & df["os"].isin(os) & df["complicaciones"].isin(complicaciones)]
elif not operador and not procedimiento and not os:
    filtered_df = df[df["metodo"].isin(metodo)]
elif not operador and not procedimiento and not complicaciones:
    filtered_df = df[df["metodo"].isin(metodo) & df["os"].isin(os)]
elif not operador and not procedimiento:
    filtered_df = df[df["metodo"].isin(metodo) & df["os"].isin(os) & df["complicaciones"].isin(complicaciones)]
elif not procedimiento and not os:
    filtered_df = df[df["operador"].isin(operador) & df["metodo"].isin(metodo)]
elif not procedimiento and not complicaciones:
    filtered_df = df[df["operador"].isin(operador) & df["metodo"].isin(metodo) & df["os"].isin(os)]
elif not procedimiento:
    filtered_df = df[df["operador"].isin(operador) & df["metodo"].isin(metodo) & df["os"].isin(os) & df["complicaciones"].isin(complicaciones)]
elif not os:
    filtered_df = df[df["operador"].isin(operador) & df["metodo"].isin(metodo) & df["procedimiento"].isin(procedimiento)]
elif not complicaciones:
    filtered_df = df[df["operador"].isin(operador) & df["metodo"].isin(metodo) & df["procedimiento"].isin(procedimiento) & df["os"].isin(os)]
elif operador:
    filtered_df = df[df["operador"].isin(operador) & df["metodo"].isin(metodo) & df["procedimiento"].isin(procedimiento) & df["os"].isin(os) & df["complicaciones"].isin(complicaciones)]

st.markdown("")
st.markdown("### Resultados:")
st.markdown("")

# Calcular el número total de registros después de aplicar los filtros
total_records = filtered_df.shape[0]
st.markdown(f"<p style='font-size:24px; font-weight:bold;'>N total: {total_records}</p>", unsafe_allow_html=True)

# Calcular el promedio de la columna "edad"
average_age = filtered_df["edad"].mean()
min_age = filtered_df["edad"].min()
max_age = filtered_df["edad"].max()

st.markdown(f"<p style='font-size:24px; font-weight:bold;'>Edad promedio: {average_age:.2f} ({min_age} - {max_age})</p>", unsafe_allow_html=True)



# Gráfico de barras ordenado por fecha
fig = px.bar(filtered_df, x="fecha", y=filtered_df.index, title="Procedimientos realizados por fecha", labels={"fecha": "Fecha", "count()": "Count", "index": "n"})
st.plotly_chart(fig)

# Gráfico de barras horizontal del número total y porcentaje del método utilizado
filtered_df["metodo"] = filtered_df["metodo"]

method_counts = filtered_df["metodo"].value_counts()
method_percentages = method_counts / method_counts.sum() * 100

method_df = pd.DataFrame({
    "Metodo": method_counts.index,
    "Total": method_counts.values,
    "Porcentaje (%)": method_percentages.values
})

fig_method = px.bar(method_df, x="Total", y="Metodo", orientation="h", text="Porcentaje (%)",
                    title="Total y Porcentaje del Método Utilizado",
                    labels={"Total": "Total", "Metodo": "Método", "Porcentaje (%)": "Porcentaje (%)"})
fig_method.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
st.plotly_chart(fig_method)

# Gráfico de barras vertical del número total y porcentaje por obra social
os_counts = filtered_df["os"].value_counts()
os_percentages = os_counts / os_counts.sum() * 100

os_df = pd.DataFrame({
    "Obra Social o Prepaga": os_counts.index,
    "Total": os_counts.values,
    "Porcentaje (%)": os_percentages.values
})

fig_os = px.bar(os_df, x="Obra Social o Prepaga", y="Total", text="Porcentaje (%)",
                title="Total y Porcentaje por Obra Social o Prepaga",
                labels={"Total": "Total", "Obra Social o Prepaga": "Obra Social o Prepaga", "Porcentaje (%)": "Porcentaje (%)"})
fig_os.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
st.plotly_chart(fig_os)

# Calcular el porcentaje de complicaciones totales
total_complications = filtered_df["complicaciones"].notnull().sum()
total_records = filtered_df.shape[0]
percentage_complications = (total_complications / total_records) * 100

st.markdown(f"<p style='font-size:24px; font-weight:bold;'>Porcentaje de complicaciones: {percentage_complications:.2f}%</p>", unsafe_allow_html=True)

# Filtrar solo las filas que tienen complicaciones diferentes de "No"
complications_table = filtered_df[filtered_df["complicaciones"] != "No"].copy()

# Seleccionar las columnas requeridas
complications_table = complications_table[["nombre", "procedimiento", "complicaciones", "resolucion"]]

# Mostrar tabla con los resultados
st.markdown("### Detalle de Complicaciones:")
st.dataframe(complications_table)