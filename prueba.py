import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')
import base64
import streamlit.components.v1 as components
os.system('pip install statsmodels')


# Configuración de página
st.set_page_config(page_title="Intervencionismo", page_icon=":bar_chart:", layout="wide")
st.title(":bar_chart: Radiologia Vascular e Intervencionista")

# Carga de archivo
fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_excel(fl)
else:
    # Cambiar la ruta según sea necesario
    df = pd.read_excel(r"C:\Users\crisa\Documents\Agustindoc\Streamlit\data.xlsx")

# Convertir columna de fecha a datetime
df["fecha"] = pd.to_datetime(df["fecha"])

# Definir columnas en Streamlit
col1, col2 = st.columns((2))

# Obtener fechas mínima y máxima
startDate = df["fecha"].min()
endDate = df["fecha"].max()

# Filtrar por fechas
with col1:
    date1 = st.date_input("Start Date", startDate.date(), min_value=startDate.date(), max_value=endDate.date())
with col2:
    date2 = st.date_input("End Date", endDate.date(), min_value=startDate.date(), max_value=endDate.date())

# Convertir los valores de date a datetime
date1 = pd.to_datetime(date1)
date2 = pd.to_datetime(date2)

# Asegurarse de que las fechas estén en el orden correcto
if date1 > date2:
    st.error("La fecha de inicio no puede ser mayor que la fecha de finalización.")
else:
    df = df[(df["fecha"] >= date1) & (df["fecha"] <= date2)].copy()
# Barra de filtros lateral
st.sidebar.header("Filtros: ")

# Filtros: Operador, Ayudante, Método, Modalidad, Procedimiento, Complicaciones, Patología, Obra Social
operador = st.sidebar.multiselect("Operador", df["operador"].unique())
ayudante = st.sidebar.multiselect("Ayudante", df["ayudante"].unique())
metodo = st.sidebar.multiselect("Método", df["metodo"].unique())
modalidad = st.sidebar.multiselect("Modalidad", df["modalidad"].unique())
procedimiento = st.sidebar.multiselect("Procedimiento", df["procedimiento"].unique())
complicaciones = st.sidebar.multiselect("Complicaciones", df["complicaciones"].unique())
patologia = st.sidebar.multiselect("Patología", df["patologia"].unique())
os = st.sidebar.multiselect("Obra Social", df["os"].unique())

# Aplicar filtros
filtered_df = df
if operador:
    filtered_df = filtered_df[filtered_df["operador"].isin(operador)]
if ayudante:
    filtered_df = filtered_df[filtered_df["ayudante"].isin(ayudante)]
if metodo:
    filtered_df = filtered_df[filtered_df["metodo"].isin(metodo)]
if modalidad:
    filtered_df = filtered_df[filtered_df["modalidad"].isin(modalidad)]
if procedimiento:
    filtered_df = filtered_df[filtered_df["procedimiento"].isin(procedimiento)]
if complicaciones:
    filtered_df = filtered_df[filtered_df["complicaciones"].isin(complicaciones)]
if patologia:
    filtered_df = filtered_df[filtered_df["patologia"].isin(patologia)]
if os:
    filtered_df = filtered_df[filtered_df["os"].isin(os)]

# Mostrar número total de registros después de aplicar filtros
st.markdown("")
st.markdown("### Resultados:")
st.markdown("")

# Definir la función para descargar el archivo CSV
def download_csv(filtered_df):
    csv = filtered_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Codificar como base64
    href = f'<a href="data:file/csv;base64,{b64}" download="filtered_data.csv">Descargar archivo CSV</a>'
    return href

# Agregar el botón para descargar el CSV
st.markdown(download_csv(filtered_df), unsafe_allow_html=True)

#Total records
total_records = filtered_df.shape[0]
st.markdown(f"<p style='font-size:24px; font-weight:bold;'>Total de registros: {total_records}</p>", unsafe_allow_html=True)

# Crear una nueva columna 'año' en el DataFrame
filtered_df['año'] = filtered_df['fecha'].dt.year

# Agrupar por año y contar el número de procedimientos
procedures_per_year = filtered_df.groupby('año').size().reset_index(name='total_procedimientos')

# Crear el gráfico de barras con línea de tendencia
fig_procedures_per_year = px.bar(procedures_per_year, x='año', y='total_procedimientos', title='Total de procedimientos por año')

# Añadir la línea de tendencia
trendline = px.scatter(procedures_per_year, x='año', y='total_procedimientos', trendline='ols').data
for trace in trendline:
    if trace.mode == 'lines':
        trace.line.color = 'red'

fig_procedures_per_year.add_traces(trendline)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig_procedures_per_year)


# Gráfico de barras ordenado por fecha
fig = px.bar(filtered_df, x="fecha", title="Procedimientos realizados por fecha")
st.plotly_chart(fig)

# Crear lista de procedimientos
procedures = [
    "Bloqueo Perirradicular", "Bloqueo Facetario", "Bloqueo Epidural", "PAAF Tiroidea", "PAAF Parotidea", 
    "PAAF Ganglionar", "Biopsia Hígado", "Biopsia Renal", "Biopsia Pulmón", "Drenaje Colección", "Drenaje Biliar", 
    "Nefrostomia", "Colecistostomia", "Verteroplastia", "Embolizacion", "TACE", "Arteriografia", "TIPS", "PICC", 
    "Gastrostomia Percutanea", "Recambio de Gastrostomia", "Bloqueo Occipital", "Angioplastia", "Biopsia Ósea", 
    "Puncion Aspiración Liquido", "Fistulografía", "Biopsia Hepática Transyugular", "Punción Biopsia", "Stent Vascular", 
    "Drenaje Ascitis y Toracentesis", "Vía Central", "Bloqueo Esplácnico", "Recambio de Nefrostomia", "Ablación por Radiofrecuencia ARF", 
    "Drenaje Neumotórax Heimlich", "Flebografía", "Marcación con Carbón", "Discogel", "Stent Biliar", "Colangiografía", 
    "Otros tipos de Bloqueos", "Infiltración", "Extracción de cuerpo extraño", "Artro RMN", "Sampling Suprarrenal", 
    "Recambio de drenaje biliar", "Catéter de Hemodialisis", "Filtro de VCI", "Recambio de Drenaje", "Cifoplastia", 
    "Cateter peritoneal / Drenaje de ascitis", "Stripping", "Radioembolización"
]

# Contar frecuencias de cada procedimiento
procedure_counts = [filtered_df[filtered_df["procedimiento"] == i + 1].shape[0] for i in range(len(procedures))]

# Crear DataFrame con los datos
procedure_df = pd.DataFrame({
    "Numero": list(range(1, len(procedures) + 1)),
    "Procedimientos": procedures,
    "n": procedure_counts
})

# Calcular el porcentaje del total de procedimientos
total_procedures = procedure_df["n"].sum()
procedure_df["%"] = (procedure_df["n"] / total_procedures) * 100

# Mostrar tabla de procedimientos
st.markdown("### Procedimientos y sus frecuencias")
st.dataframe(procedure_df.set_index("Numero"))

# Calcular el número y porcentaje de pacientes pediátricos y adultos
pediatric_count = filtered_df[filtered_df["edad"] <= 15].shape[0]
adult_count = filtered_df[filtered_df["edad"] > 15].shape[0]
total_patients = pediatric_count + adult_count

percentage_pediatric = (pediatric_count / total_patients) * 100
percentage_adult = (adult_count / total_patients) * 100

# Crear un DataFrame para el gráfico
patients_df = pd.DataFrame({
    "Grupo Etario": ["Pediátricos (<=15 años)", "Adultos (>15 años)"],
    "Número de Pacientes": [pediatric_count, adult_count],
    "Porcentaje": [percentage_pediatric, percentage_adult]
})

# Gráfico de barras verticales
fig_patients = px.bar(patients_df, x="Grupo Etario", y="Número de Pacientes", text="Porcentaje",
                      title="Número y Porcentaje de Pacientes por Grupo Etario",
                      labels={"Grupo Etario": "Grupo Etario", "Número de Pacientes": "Número de Pacientes", "Porcentaje": "Porcentaje (%)"})
fig_patients.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
st.plotly_chart(fig_patients)

# Mostrar tabla con el número de pacientes y porcentaje
st.markdown("### Número y Porcentaje de Pacientes por Grupo Etario")
st.dataframe(patients_df.set_index("Grupo Etario"))

# Gráfico de barras horizontales del número y porcentaje de procedimientos por operador
operator_procedure_counts = filtered_df.groupby(["operador", "procedimiento"]).size().reset_index(name="counts")
operator_procedure_counts = operator_procedure_counts.merge(procedure_df[["Numero", "Procedimientos"]], left_on="procedimiento", right_on="Numero", how="left")
operator_procedure_counts["Porcentaje"] = (operator_procedure_counts["counts"] / operator_procedure_counts.groupby("operador")["counts"].transform("sum")) * 100

fig_operator_procedures = px.bar(operator_procedure_counts, x="counts", y="operador", color="Procedimientos", orientation="h",
                                 title="Número y Porcentaje de Procedimientos por Operador",
                                 labels={"counts": "Número de Procedimientos", "operador": "Operador", "Porcentaje": "Porcentaje"})
fig_operator_procedures.update_traces(texttemplate='%{x:.0f}', textposition='outside')
st.plotly_chart(fig_operator_procedures)

# Calcular número total y porcentaje de procedimientos realizados por cada operador
total_procedures_by_operator = filtered_df["operador"].value_counts().reset_index()
total_procedures_by_operator.columns = ["Operador", "n"]
total_procedures_by_operator["Porcentaje"] = (total_procedures_by_operator["n"] / total_procedures_by_operator["n"].sum()) * 100

# Añadir fila con el total de procedimientos
total_row = pd.DataFrame([{
    "Operador": "Total",
    "n": total_procedures_by_operator["n"].sum(),
    "Porcentaje": total_procedures_by_operator["Porcentaje"].sum()
}])
total_procedures_by_operator = pd.concat([total_procedures_by_operator, total_row], ignore_index=True)

# Mostrar tabla en Streamlit
st.markdown("### Número Total y Porcentaje de Procedimientos por Operador")
st.dataframe(total_procedures_by_operator)

# Tabla con los 5 procedimientos más realizados por cada operador
top5_procedures_by_operator = operator_procedure_counts.groupby("operador").apply(lambda x: x.nlargest(5, "counts")).reset_index(drop=True)

# Mostrar tabla en Streamlit
st.markdown("### Top 5 Procedimientos por Operador")
for operator in top5_procedures_by_operator["operador"].unique():
    st.markdown(f"#### {operator}")
    top5_for_operator = top5_procedures_by_operator[top5_procedures_by_operator["operador"] == operator][["Procedimientos", "counts", "Porcentaje"]]
    top5_for_operator = top5_for_operator.rename(columns={"Procedimientos": "Procedimiento", "counts": "Cantidad", "Porcentaje": "Porcentaje (%)"})
    st.dataframe(top5_for_operator)


# Gráfico de barras verticales del número total y porcentaje de la columna "modalidad"
modalidad_counts = filtered_df["modalidad"].value_counts()
modalidad_percentages = modalidad_counts / modalidad_counts.sum() * 100
modalidad_df = pd.DataFrame({
    "Modalidad": modalidad_counts.index,
    "Total": modalidad_counts.values,
    "Porcentaje (%)": modalidad_percentages.values
})
fig_modalidad = px.bar(modalidad_df, x="Modalidad", y="Total", text="Porcentaje (%)",
                       title="Total y Porcentaje de Modalidades",
                       labels={"Modalidad": "Modalidad", "Total": "Total", "Porcentaje (%)": "Porcentaje (%)"})
fig_modalidad.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig_modalidad.update_layout(xaxis_title="Modalidad", yaxis_title="Total")
st.plotly_chart(fig_modalidad)


# Gráfico de barras horizontal del número total y porcentaje del método utilizado
method_counts = filtered_df["metodo"].value_counts()
method_percentages = method_counts / method_counts.sum() * 100
method_df = pd.DataFrame({
    "Método": method_counts.index,
    "Total": method_counts.values,
    "Porcentaje (%)": method_percentages.values
})
fig_method = px.bar(method_df, x="Total", y="Método", orientation="h", text="Porcentaje (%)",
                    title="Total y Porcentaje del Método Utilizado",
                    labels={"Total": "Total", "Método": "Método", "Porcentaje (%)": "Porcentaje (%)"})
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
total_complications = filtered_df[filtered_df["complicaciones"] != "No"].shape[0]
percentage_complications = (total_complications / total_records) * 100
st.markdown(f"<p style='font-size:24px; font-weight:bold;'>Porcentaje de complicaciones: {percentage_complications:.2f}%</p>", unsafe_allow_html=True)

# Filtrar complicaciones y mostrar detalle en tabla
complications_table = filtered_df[filtered_df["complicaciones"] != "No"][["nombre", "procedimiento", "complicaciones", "resolucion"]]
st.markdown("### Detalle de Complicaciones:")
st.dataframe(complications_table)

def plot_complications(df, procedure_id, procedure_name):
    df_procedure = df[df["procedimiento"] == procedure_id][["procedimiento", "complicaciones", "nombre", "resolucion", "patologia"]].copy()
    df_procedure["procedimiento"] = procedure_name
    df_procedure["complicaciones"] = df_procedure["complicaciones"].replace("No", "No Complicaciones")
    complication_counts = df_procedure["complicaciones"].value_counts()
    complication_percentages = complication_counts / complication_counts.sum() * 100
    total_procedures = len(df_procedure)  # Número total de procedimientos para este procedimiento

    complications = pd.DataFrame({
        "Complicaciones": complication_counts.index,
        "Total Complicaciones": complication_counts.values,
        "Porcentaje Complicaciones (%)": complication_percentages.values
    })

    title_text = f"{procedure_name}:          \nN total: {total_procedures}"

    fig_complications = px.bar(complications, x="Total Complicaciones", y="Complicaciones", orientation="h", text="Porcentaje Complicaciones (%)",
                               title=title_text,
                               labels={"Total Complicaciones": "Total Complicaciones", "Complicaciones": "Complicaciones", "Porcentaje Complicaciones (%)": "Porcentaje Complicaciones (%)"})
    fig_complications.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    st.markdown(f"### {procedure_name}")
    st.plotly_chart(fig_complications)

    complications_table = df_procedure[df_procedure["complicaciones"] != "No Complicaciones"][["nombre", "complicaciones", "resolucion"]]
    st.markdown(f"### Detalle de Complicaciones - {procedure_name}")
    st.dataframe(complications_table)

    # Nueva tabla para mostrar el nombre del paciente y la patología
    pathology_table = df_procedure[["nombre", "patologia"]]
    pathology_table = pathology_table.drop_duplicates()  # Eliminar duplicados por si hay varios procedimientos para el mismo paciente
    st.markdown(f"### Detalle de Patología - {procedure_name}")
    st.dataframe(pathology_table)

# Títulos antes de cada sección
plot_complications(df, 7, "Biopsia Hepática")

plot_complications(df, 8, "Biopsia Renal")

plot_complications(df, 9, "Biopsia Pulmonar")

# Título y gráfico de barras verticales para el procedimiento "PAAF Tiroidea"
procedure_name = "PAAF Tiroidea"
procedure_id = 4  # Número de procedimiento para PAAF Tiroidea
df_procedure = filtered_df[filtered_df["procedimiento"] == procedure_id]
total_procedures = df_procedure.shape[0]

st.markdown(f"### {procedure_name}")
st.markdown(f"N total: {total_procedures}")

# Calcular número de casos y porcentaje por patología
patologia_counts = df_procedure["patologia"].value_counts()
patologia_percentages = patologia_counts / patologia_counts.sum() * 100

# Crear DataFrame con los datos de patologías
patologia_df = pd.DataFrame({
    "Patología": patologia_counts.index,
    "Número de casos": patologia_counts.values,
    "Porcentaje (%)": patologia_percentages.values.round(2)
})

# Ordenar la tabla por el número de casos (ascendente)
patologia_df = patologia_df.sort_values(by="Patología", ascending=True)

# Reasignar el índice para que comience desde 1
patologia_df.index = range(1, len(patologia_df) + 1)

# Gráfico de barras verticales
fig = px.bar(patologia_df, x=patologia_df.index, y="Número de casos", 
             title="Distribución de Patologías para PAAF Tiroidea",
             labels={"x": "Patología", "Número de casos": "Número de casos"})
fig.update_layout(xaxis_title="Patología", yaxis_title="Número de casos")
fig.update_traces(text=patologia_df["Porcentaje (%)"].astype(str) + '%')
st.plotly_chart(fig)

# Mostrar tabla con el número de casos y porcentaje por patología ordenada
st.markdown("### Detalle de Patologías:")
st.dataframe(patologia_df.set_index("Patología"))


