def preencherInfoListas(dataframesDivididos, filial, secao):
    num_eventos = []
    eventos = []
    valores = []
    tipos = []
    setores = []
    filiais = []

    def proventos(df_prov_desc):
        virgula = ','
        df_prov_desc.rename(columns={df_prov_desc.columns[2]: 'b'}, inplace=True)
        if filial in ['AUT', 'PLB']:
            df_prov_desc = df_prov_desc.drop(['b'], axis=1)

        for row in df_prov_desc.values:
            if (str(row[0]) == 'nan') or (str(row[0].split(' ')[0]) == 'Proventos:'):
                break
            if int(len(str(row[1]).split(' '))) < 2:
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

    def descontos(df_prov_desc):
        virgula = ','
        df_prov_desc.rename(columns={df_prov_desc.columns[2]: 'b'}, inplace=True)
        if filial in ['AUT', 'PLB']:
            df_prov_desc = df_prov_desc.drop(['b'], axis=1)

        for row in df_prov_desc.values:
            a = len(str(row[1]).split(' '))
            if (str(row[1]).split(' ')[0] == 'Descontos:') or (len(str(row[1]).split(' ')) < 3 and str(row[2]).split(' ')[0] == 'nan'):
                break
            if (virgula not in str(row[1]).split(' ')[0]) and (str(row[0]).split(' ')[0] == 'nan') and (len(str(row[1]).split(' ')) < 2):
                eventos.append(str(row[1]) + ' ' + str(row[2]))
                num_eventos.append(row[1].split(' ')[0])
            else:
                if virgula in str(row[1].split(' ')[1]):
                    eventos.append(' '.join(row[1].split(' ')[2:a]))
                    num_eventos.append(row[1].split(' ')[2])
                elif virgula not in str(row[1].split(' ')[0]):
                    eventos.append(' '.join(row[1].split(' ')[0:a]))
                    num_eventos.append(row[1].split(' ')[0])
                else:
                    eventos.append(' '.join(row[1].split(' ')[1:a]))
                    num_eventos.append(row[1].split(' ')[1])
            if int(len(str(row[3]).split(' '))) > 1:
                valores.append('-' + str(row[3].split(' ')[1]))
            else:
                valores.append('-' + str(row[3]))
            tipos.append('DESCONTOS')
            setores.append(secao)
            filiais.append(filial)

    def fgts(df_fgts):
        num_eventos.append('F.G.T.S.')
        eventos.append('F.G.T.S.')
        tipos.append('FGTS')
        setores.append(secao)
        filiais.append(filial)
        if (filial in ['SP', 'PL']) and (str(df_fgts.iloc[0][2]) == 'nan'):
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
            valores.append(str(df_fgts.iloc[0][1]).split(' ')[1])
            salario = df_fgts.iloc[1][1].split(': ')[1]
            if salario != '0,00':
                num_eventos.append('F.G.T.S. 13o. Salário')
                eventos.append('F.G.T.S. 13o. Salário')
                tipos.append('FGTS')
                valores.append(str(salario))
                setores.append(secao)
                filiais.append(filial)

    def gps(df_gps):
        num_eventos.append('INSS EMPRESA')
        eventos.append('INSS EMPRESA.')
        tipos.append('INSS')
        setores.append(secao)
        filiais.append(filial)
        valores.append(str(df_gps.iloc[0][1]).split(' ')[0])

        if filial not in ['AUT', 'PLB']:
            num_eventos.append('INSS TERCEIROS')
            eventos.append('INSS TERCEIROS.')
            tipos.append('INSS')
            valores.append(str(df_gps.iloc[1][1]))
            setores.append(secao)
            filiais.append(filial)

    # --- Execução ---
    proventos(dataframesDivididos[0])
    descontos(dataframesDivididos[0])
    if filial in ['AUT', 'PLB']:
        gps(dataframesDivididos[1])
    else:
        fgts(dataframesDivididos[1])
        gps(dataframesDivididos[2])

    return [num_eventos, eventos, valores, tipos, filiais, setores]
