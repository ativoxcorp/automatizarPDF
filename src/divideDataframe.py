import pandas as pd

def divideDataframe(resumo_secao,filial):
    proventos = 'Proventos'
    fgts_mensal = 'FGTS Mensal'
    gps = 'G P S'

#Divide o dataframe(resumo_secao) em três(df_prov_desc,df_fgts,df_gps)
    for index, row in resumo_secao.iterrows():
        if proventos in str(row[0]):
            df_prov_desc = resumo_secao[index+1:index*5]

            proventos = 'kkkkkkkkk9999dfdgerrs24a1a2a55'
        if gps in str(row[1]) or gps in str(row[2]):

            df_gps = resumo_secao[index+2:index+4]
            gps = 'kkkkkkkkk9999dfdgerrs24a1a2a55'

        if fgts_mensal in str(row[1]):

            df_fgts = resumo_secao[index+1:index+3]

            fgts_mensal = 'kkkkkkkkk9999dfdgerrs24a1a2a55'

    if filial == 'AUT' or filial == 'PLB':
        dataframes =  [df_prov_desc, df_gps]
        #print('geregere')
        ##print(df_prov_desc)
        #df_prov_desc.to_excel("df_prov_desc.xlsx")
        #df_gps.to_excel("df_gps.xlsx")
    else:
        dataframes =  [df_prov_desc, df_fgts, df_gps]

    return dataframes