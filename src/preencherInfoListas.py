

num_eventos = []
eventos = []
valores = []
tipos = []
setores = []
filiais = []

def preencherInfoListas(dataframesDivididos,filial,secao):


    proventos(dataframesDivididos[0],filial,secao)
    descontos(dataframesDivididos[0],filial,secao)
    if filial == 'AUT' or filial == 'PLB':
        gps(dataframesDivididos[1],filial,secao)
    else:

        fgts(dataframesDivididos[1],filial,secao)
        gps(dataframesDivididos[2],filial,secao)


    return [num_eventos, eventos, valores, tipos, filiais, setores]




def proventos(df_prov_desc,filial,secao):
    virgula = ','

    df_prov_desc.rename(columns = {df_prov_desc.columns[1]:'b'}, inplace = True)
    if filial == 'AUT' or filial == 'PLB':
        df_prov_desc = df_prov_desc.drop(['b'], axis=1 )

    for row in df_prov_desc.values:
        if (str(row[0]) == 'nan') or (str(row[0].split(' ')[0]) == 'Proventos:'):
            break
        if int(len(str(row[1]).split(' '))) < 2 :
             valores.append(str(row[1]).split(' ')[0])
        else:
            if virgula in str(row[1].split(' ')[1]):
                valores.append(str(row[1]).split(' ')[1])
            else:
                valores.append(str(row[1]).split(' ')[0])
        evento = str(row[0])
        eventos.append(evento)
        num_eventos.append(row[0].split(' ')[0])
        tipos.append('PROVENTOS')
        setores.append(secao)
        filiais.append(filial)

def descontos(df_prov_desc,filial,secao):
    virgula = ','
    #df_prov_desc.rename(columns = {df_prov_desc.columns[1]:'b'}, inplace = True)
    if filial == 'AUT' or filial == 'PLB':
        df_prov_desc.rename(columns = {df_prov_desc.columns[1]:'b'}, inplace = True)
        df_prov_desc = df_prov_desc.drop(['b'], axis=1 )

    for row in df_prov_desc.values:
        a = len(str(row[1]).split(' '))
        if (str(str(row[1]).split(' ')[0]) == 'Descontos:') or (str(row[1]).split(' ')[0] == 'nan') or (len(str(row[1]).split(' ')) < 3 and str(row[2]).split(' ')[0] == 'nan'):
            break
        if (virgula not in str(row[1]).split(' ')[0]) and (str(row[0]).split(' ')[0] == 'nan') and (len(str(row[1]).split(' ')) < 2):
            eventos.append(str(row[1]) + ' ' + str(row[2]))
            num_eventos.append(row[1].split(' ')[0])
        else:

            if virgula in str(row[1].split(' ')[1]):
                eventos.append(' '.join([str(item) for item in row[1].split(' ')[2:a]]))
                num_eventos.append(row[1].split(' ')[2])
            elif virgula not in str(row[1].split(' ')[0]):
                eventos.append(' '.join([str(item) for item in row[1].split(' ')[0:a]]))
                num_eventos.append(row[1].split(' ')[0])
            else:
                eventos.append(' '.join([str(item) for item in row[1].split(' ')[1:a]]))
                num_eventos.append(row[1].split(' ')[1])
        if int(len(str(row[3]).split(' '))) > 1:
            valores.append('-' + str(row[3].split(' ')[1]))
        else:
            valores.append('-' + str(row[3]))
        tipos.append('DESCONTOS')
        setores.append(secao)
        filiais.append(filial)

def fgts(df_fgts,filial,secao):
    num_eventos.append('F.G.T.S.')
    eventos.append('F.G.T.S.')
    tipos.append('FGTS')
    setores.append(secao)
    filiais.append(filial)
    if (filial == 'SP' or filial == 'PL') and (str(df_fgts.iloc[0][2]) == 'nan'):
        valores.append(str(df_fgts.iloc[0][3]).split(' ')[0])
        salario = str(df_fgts.iloc[1][3])
        if salario != '0,00':
            num_eventos.append('F.G.T.S. 13o. Salário')
            eventos.append('F.G.T.S. 13o. Salário')
            tipos.append('FGTS')
            valores.append(str(salario))
            setores.append(secao)
            filiais.append(filial)
    else:
        if len(str(df_fgts.iloc[0][1]).split(' ')) < 2:
            if (filial == 'RJ') and (str(df_fgts.iloc[0][1]) == 'F.G.T.S.:') and (str(df_fgts.iloc[0][2]) != 'nan') and (str(df_fgts.iloc[1][2]) != 'nan'):
                valores.append(str(df_fgts.iloc[0][2]))
            elif (filial == 'RJ') and (str(df_fgts.iloc[0][1]) == 'F.G.T.S.:') and (str(df_fgts.iloc[0][2]) == 'nan') and (str(df_fgts.iloc[1][2]) == 'nan'):
                valores.append(str(df_fgts.iloc[0][3]).split()[0])
            else:
                valores.append(str(df_fgts.iloc[0][2]))

        else:
            if (filial == 'RJ') and (str(df_fgts.iloc[0][1]) == '0,00 F.G.T.S.:') and (str(df_fgts.iloc[0][2]) == '0,00') and (str(df_fgts.iloc[1][2]) == '0,00'):
                valores.append(str(df_fgts.iloc[0][2]))
            else:
                valores.append(str(df_fgts.iloc[0][1]).split(' ')[1])
        #setores.append(secao)
        #filiais.append(filial)

        if len(str(df_fgts.iloc[1][1]).split(': ')) < 2:
            if (filial == 'RJ') and (len(str(df_fgts.iloc[1][0]).split(': ')) < 2) and (str(df_fgts.iloc[0][2]) != 'nan') and (str(df_fgts.iloc[1][2]) != 'nan'):
                salario = df_fgts.iloc[1][2]
            elif (filial == 'RJ') and (len(str(df_fgts.iloc[1][0]).split(': ')) < 2) and (str(df_fgts.iloc[0][2]) == 'nan') and (str(df_fgts.iloc[1][2]) == 'nan'):
                salario = df_fgts.iloc[1][3]
            else:
                salario = df_fgts.iloc[1][2]
        else:
            salario = df_fgts.iloc[1][1].split(': ')[1]
        if salario != '0,00':
            num_eventos.append('F.G.T.S. 13o. Salário')
            eventos.append('F.G.T.S. 13o. Salário')
            tipos.append('FGTS')
            valores.append(str(salario))
            setores.append(secao)
            filiais.append(filial)

def gps(df_gps,filial,secao):
    num_eventos.append('INSS EMPRESA')
    eventos.append('INSS EMPRESA.')
    tipos.append('INSS')
    setores.append(secao)
    filiais.append(filial)
    #--
    if filial == 'AUT' or filial == 'PLB':
        if filial == 'AUT':
            valores.append(str(df_gps.iloc[0][2]).split(' ')[0])
        else:
            valores.append(str(df_gps.iloc[0][1]).split(' ')[0])
    else:
        valores.append(str(df_gps.iloc[0][1]).split(' ')[0])
        num_eventos.append('INSS TERCEIROS')
        eventos.append('INSS TERCEIROS.')
        tipos.append('INSS')
        valores.append(str(df_gps.iloc[1][1]))
        setores.append(secao)
        filiais.append(filial)
