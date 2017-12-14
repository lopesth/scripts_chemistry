# -*- coding: UTF-8 -*-

'''
Thiago Lopes - 11:16 de 13/06/17
Programa para selecionar "aleatoriamente" as questões para prova para cada Aluno
'''

import random

def seleciona_questao(lista_alvo, elementos_totais):
	numero = 100000
	while numero not in lista_alvo:
		numero = random.randint(1, elementos_totais)
	lista_alvo.remove(numero)
	return numero

alunos_ = ["Ueslei Vasconcelos", "Fernanda Ferrari", "Brenda Sperandio", "Camila Dourado", "Esdras Figueredo", "Fernando Monteiro", "Gabriel Dutra", "Hadassa Ramos", "Michele Avila dos Santos", "Pedro Heitor Rodrigues Fernandes", "Priscila Rios Teixeira"]
alunos = []
for aluno in alunos_:
	aluno_new = str(random.randint(1,11))+'-'+aluno
	alunos.append(aluno_new)

numero_de_questoes = int(input("Qual a quantidade de questoes?  "))
questoes = list(range(1,numero_de_questoes +1, 1))
relacao = {}
resposta = "s"

remover = input("Deseja remover alguma questao?  ")
print("\n\n")
if remover in ["sim", "s", "Sim", "y", "Yes"]:
	questoes_a_remover = input("Coloque as questoes a serem removidas separadas pro virgulas -> ").split(",")
	print ("Irei remover as questoes %s da lista %s" %(questoes_a_remover, questoes), end='\n\n')
	for remocao_str in questoes_a_remover:
		remocao = int(remocao_str)
		questoes.remove(remocao)
	print ("Ficaram as questoes %s no jogo." %questoes, end='\n\n')

ordem_de_jogada = 1	

while(resposta not in ["n", "N", "Não", "não", "no", "No", "nao"]):
	for aluno in alunos:
		escolha = str(seleciona_questao(questoes, numero_de_questoes))
		relacao.update({aluno:"Question "+escolha})
	for chave in relacao.keys():
		print("Jogador numero %d" %ordem_de_jogada, end='\n\n')
		ordem_de_jogada+=1
		print (chave.split("-")[-1]+":\n    "+relacao[chave]+"\n")
		resposta_espera = "zzzzzzz"
		while resposta_espera != "ok":
			resposta_espera = input("Digite OK para o próximo aluno ->  ")
			print('\n\n')
	
	resposta = input("Deseja rodar novamente? s para Sim e n para Não -> ")
	if resposta not in ["n", "N", "Não", "não", "no", "No"]:
		print ("Ok, sobraram as questões %s, vamos rodar novamente e ver quem fica com qual." %(questoes), end='\n\n')
	else:
		print ("Ok, boa sorte.")


