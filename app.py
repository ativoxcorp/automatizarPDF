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
        if files is not None:
                files.append(files.pop(0))
                for file in files:
                        #print('aaaaa')
                        #print(file)
                        dfs = tabula.read_pdf(file, encoding = 'ISO-8859-1', pages='all')
                        #print('bbbbb')
                        #print(dfs)
                        df = pd.DataFrame([dfs], dtype=object)
                        #print(df)
                        #print('-------')
                        #df.iloc[0][1].to_excel('resumo.xlsx', index=False)
                        #print(df.iloc[0][1])
                        palavra_chave = 'R E S U M O Secao:'
                        for index in range(len(df.columns)-1):
                                if palavra_chave in str(df.iloc[0][index].iloc[3][1]) or palavra_chave in str(df.iloc[0][index].iloc[3][0]):
                                        resumo = df.iloc[0][index]
                                        #print(resumo.shape)
                                        resumo.rename(columns = {resumo.columns[0]:'a',resumo.columns[1]:'b', resumo.columns[2]:'c',
                                                                resumo.columns[3]:'d'}, inplace = True) #resumo.columns[4]:'e'
                                        #resumo_secao = resumo.drop(['c', 'd'], axis=1)
                                        #print('aaaaa')
                                        #print(resumo.columns)
                                        #resumo.to_excel('resumo.xlsx', index=False)
                                        data = str(resumo.iloc[1][3]).split(' ')[2]
                                        periodo = str(resumo.iloc[1][3]).split(' ')[2][-7:]
                                        filial = str(resumo.iloc[0][0]).split(' ')[1][-2:]
                                        #print(str(df.iloc[0][index].iloc[3][1]))
                                        if str(df.iloc[0][index].iloc[3][1]) == 'nan':
                                                secao = str(resumo.iloc[3][0]).split(': ')[1]
                                        else:
                                                secao = str(resumo.iloc[3][1]).split(': ')[1]

                                        dataframesDivididos = divideDataframe.divideDataframe(resumo,filial)
                                        infListas = preencherInfoListas.preencherInfoListas(dataframesDivididos,filial,secao)

                                #print('aaaa')
                                #df.iloc[0][1].to_excel("teste.xlsx")
                                #print(str(df.iloc[0][1].iloc[3][1]).replace(' ', ''))    
                                if str(df.iloc[0][1].iloc[3][1]).replace(' ', '') == 'RESUMO':
                                        #print('aaaaa')
                                        resumo = df.iloc[0][1]
                                        #resumo.to_excel('resumo.xlsx', index=False)
                                        #print(resumo)
                                        data = str(resumo.iloc[1][4]).split(' ')[2]
                                        #print(data)
                                        #print('----')
                                        periodo = str(resumo.iloc[1][4]).split(' ')[2][-7:]
                                        #print(periodo)
                                        if resumo.columns[0] == 'Folha de Autônomos':
                                                filial = 'AUT'
                                                secao = 'AUTONOMO'
                                        else:
                                                filial = 'PLB'
                                                secao = 'PRO-LABORE'  
                                        dataframesDivididos = divideDataframe.divideDataframe(resumo,filial)
                                        infListas = preencherInfoListas.preencherInfoListas(dataframesDivididos,filial,secao)
                #print(dataframesDivididos)
                d = {'FILIAL':infListas[4],'SETOR':infListas[5],
                     'TIPO':infListas[3],'N° Evento':infListas[0], 
                     'Descrição Evento':infListas[1], 'VALOR':infListas[2]}
                                

                formatado = pd.DataFrame(d)
                formatado.insert(0,'DATA',data)
                formatado.insert(1,'PERÍODO',periodo)
                final = formatado.replace({'FILIAL': {'ON': 'MA'}})
                #files.clear()
                st.cache_resource.clear()
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                        final.to_excel(writer, index=False, sheet_name='Sheet1')
                #writer.close()
                #final = final.iloc[0:0]
                processed_data = buffer.getvalue()
                st.download_button(
                        label="Download Excel worksheets",
                        data=buffer,
                        file_name="pdfToExcel.xlsx",
                        mime="application/vnd.ms-excel")
                writer.close()
        else:
               st.info("Anexar documento")
               
