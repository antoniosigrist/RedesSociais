# encoding: utf-8

import pandas as pd

ano_lista = [1970,1980,1990,2000,2010,2017]

for year in ano_lista:

	ano = str(year)

	file = open('year_'+ano+'.gml','w') 


	df = pd.read_csv(r'pop_refugiada - y-'+ano+'.csv', encoding='utf-8')
	df2 = pd.read_csv(r'%import_pib - %arm_pib.csv', encoding='utf-8')

	id_node = 0
	countries = []
	dic = {} 

	file.write('graph ['+'\n') 
	file.write('  directed 1'+'\n')

	# Adiciona na lista countries todos os países (nós) que haverão no programa

	for index, row in df.iterrows():

		if row['Origin'] in countries:

			pass

		else:

			if row['Origin'] != 'Various/Unknown':

				countries.append(row['Origin'])

		if row['Country / territory of asylum/residence'] in countries:

			pass

		else:

			if row['Country / territory of asylum/residence'] != 'Various/Unknown':
				countries.append(row['Country / territory of asylum/residence'])



	## Cria todos os nodes no arquivo .gml
	paises_escritos = []

	for pais in countries:

		for index, row in df2.iterrows():
			#print (index)
			
			if row['Country Name'] == pais and row['Series Name'] == 'Armed forces personnel':

				armed_force = row[ano][index]

			else: 

				armed_force = 0


			if row['Country Name'] == pais and row['Series Name'] == 'Arms imports (SIPRI trend indicator values)':
			#	print("Entrou 1")
				imports = (row['[YR' + ano + ']'])

				if imports == "..":
					imports = 0
				file.write('  node ['+'\n') 
				file.write('    id '+ str(id_node)+'\n')
				file.write('    label '+'"'+str(pais) + '"'+'\n')
				file.write('    armed_force '+'"'+str(armed_force) + '"'+'\n')
				if imports == 'nan':
					imports = 0
				file.write('    imports '+'"'+str(imports) + '"'+'\n')
				id_node += 1
				file.write('  ]'+'\n')
				paises_escritos.append(str(pais))
			else: 
			#	print("Entrou 2")
				imports = 0
			#print(armed_force)
			#print(imports)
		if pais not in paises_escritos:
				file.write('  node ['+'\n') 
				file.write('    id '+ str(id_node)+'\n')
				file.write('    label '+'"'+str(pais) + '"'+'\n')
				file.write('    armed_force '+'"'+str(armed_force) + '"'+'\n')
				if imports == 'nan':
					imports = 0
				file.write('    imports '+'"'+ "0" + '"'+'\n')
				id_node += 1
				file.write('  ]'+'\n')		


	 
	print('Realizou .gml do ano '+ano)
	#Adiciona todos as possíveis origens e destino em um dicionário para evitar edges repetidas
	for index, row in df.iterrows():


		if str(row['Origin']) != 'Various/Unknown' and str(row['Country / territory of asylum/residence']) != 'Various/Unknown':

			if ('"' + str(row['Origin']) + ' -> ' + str(row['Country / territory of asylum/residence'])+'"') not in dic:
				dic['"' + str(row['Origin']) + ' -> ' + str(row['Country / territory of asylum/residence'])+'"'] = [[float(row['%'])],0]
			else:
				try:
					dic['"' + str(row['Origin']) + ' -> ' + str(row['Country / territory of asylum/residence'])+'"'][0].append(float(row['%'])/1.0)
					#print("Entrou aqui")
				except:
					dic['"' + str(row['Origin']) + ' -> ' + str(row['Country / territory of asylum/residence'])+'"'][0].append(0.0)
					#print("Deu erro")


	## Cria todas as edges existentes no arquivo .gml trocando a posicao dic[1] = 1 para mostrar que aquele destino já foi preenchido e evitar repetição
	for index, row in df.iterrows():

		if str(row['Origin']) != 'Various/Unknown' and str(row['Country / territory of asylum/residence']) != 'Various/Unknown':
		
			if dic['"' + str(row['Origin']) + ' -> ' + str(row['Country / territory of asylum/residence'])+'"'][1] == 0:
				file.write('  edge ['+'\n') 
				file.write('    source '+ str(countries.index(row['Origin']))+'\n')
				file.write('    target '+ str(countries.index(row['Country / territory of asylum/residence']))+'\n')
				file.write('    label '+ '"' + str(row['Origin']) + ' -> ' + str(row['Country / territory of asylum/residence'])+'"'+'\n')
				if str((sum(dic['"' + str(row['Origin']) + ' -> ' + str(row['Country / territory of asylum/residence'])+'"'][0]))) == 'nan':
					file.write('    weight 0')
				else:
					#print((sum(dic['"' + str(row['Origin']) + ' -> ' + str(row['Country / territory of asylum/residence'])+'"'][0])))
					file.write('    weight ' + str(sum(dic['"' + str(row['Origin']) + ' -> ' + str(row['Country / territory of asylum/residence'])+'"'][0]))+'\n')
				file.write('  ]'+'\n')
				dic['"' + str(row['Origin']) + ' -> ' + str(row['Country / territory of asylum/residence'])+'"'][1] = 1
	#print(dic)
	file.write(']'+'\n')


	file.close() 