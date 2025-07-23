'''
import streamlit as st
import tabula
from tabula.util import java_version
import pandas as pd
import numpy as np
from io import BytesIO
import xlsxwriter
import src.divideDataframe as divideDataframe
import src.preencherInfoListas as preencherInfoListas

st.set_page_config(page_title="AutomatizarPDF", page_icon="✅", layout="centered")
st.title("Converter PDF para planilha | Exportar excel!")

form = st.form(key="integration")

with form:
        cols = st.columns(1)
        #cols = st.columns(2)
        #inicio_depreciacao = cols[0].date_input("Início da depreciação:")
        files = st.file_uploader("Selecionar arquivo(s) .pdf", accept_multiple_files=True)
        submitted = st.form_submit_button(label="Submit")

if submitted:
    if files is not None and len(files) > 0:
        resultados = []  # <--- lista para garantir dados "novos" a cada execução
        for file in files:
            dfs = tabula.read_pdf(file, encoding='ISO-8859-1', pages='all')
            df = pd.DataFrame([dfs], dtype=object)
            palavra_chave = 'R E S U M O Secao:'
            
            for index in range(len(df.columns)-1):
                if palavra_chave in str(df.iloc[0][index].iloc[3][1]) or palavra_chave in str(df.iloc[0][index].iloc[3][0]):
                    resumo = df.iloc[0][index]
                    resumo.rename(columns={
                        resumo.columns[0]: 'a',
                        resumo.columns[1]: 'b',
                        resumo.columns[2]: 'c',
                        resumo.columns[3]: 'd'
                    }, inplace=True)

                    data = str(resumo.iloc[1][3]).split(' ')[2]
                    periodo = data[-7:]
                    filial = str(resumo.iloc[0][0]).split(' ')[1][-2:]

                    secao = str(resumo.iloc[3][1]).split(': ')[1] if str(df.iloc[0][index].iloc[3][1]) != 'nan' else str(resumo.iloc[3][0]).split(': ')[1]

                    dataframesDivididos = divideDataframe.divideDataframe(resumo, filial)
                    infListas = preencherInfoListas.preencherInfoListas(dataframesDivididos, filial, secao)
                    resultados.append((data, periodo, infListas))

                if str(df.iloc[0][1].iloc[3][1]).replace(' ', '') == 'RESUMO':
                    resumo = df.iloc[0][1]
                    data = str(resumo.iloc[1][4]).split(' ')[2]
                    periodo = data[-7:]
                    filial = 'AUT' if resumo.columns[0] == 'Folha de Autônomos' else 'PLB'
                    secao = 'AUTONOMO' if filial == 'AUT' else 'PRO-LABORE'

                    dataframesDivididos = divideDataframe.divideDataframe(resumo, filial)
                    infListas = preencherInfoListas.preencherInfoListas(dataframesDivididos, filial, secao)
                    resultados.append((data, periodo, infListas))

        # Após processar todos os arquivos:
        linhas = []
        for data, periodo, infListas in resultados:
            for i in range(len(infListas[0])):
                linhas.append({
                    'DATA': data,
                    'PERÍODO': periodo,
                    'N° Evento': infListas[0][i],
                    'Descrição Evento': infListas[1][i],
                    'VALOR': infListas[2][i],
                    'TIPO': infListas[3][i],
                    'FILIAL': infListas[4][i],
                    'SETOR': infListas[5][i]
                })

        final_df = pd.DataFrame(linhas)
        final_df.replace({'FILIAL': {'ON': 'MA'}}, inplace=True)

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            final_df.to_excel(writer, index=False, sheet_name='Sheet1')
            writer.close()

        st.download_button(
            label="Download Excel worksheets",
            data=buffer,
            file_name="pdfToExcel.xlsx",
            mime="application/vnd.ms-excel"
        )

    else:
        st.info("Anexar documento")
               

               
'''