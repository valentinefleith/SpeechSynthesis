mot_phonetique$ = "vodka"
longueur_mot = length(mot_phonetique$)

	#for a from 1 to longueur_mot - 1
		#diphone$ = mid$(mot_phonetique$, a, 2)
		diphone$ = mid$(mot_phonetique$, 1, 2)
		phoneme1$ = mid$(diphone$, 1, 1)
		phoneme2$ = mid$(diphone$, 2, 1)
		#diphone$ = phoneme$ + ".wav"

		#son'a' = Read from file:  chemin$ + phoneme$ 

	#endfor

nom$ = "faure"
son$ = nom$ + ".wav"
grille$ = nom$ + ".TextGrid"

son = Read from file: son$
grille = Read from file: grille$

# Ces 4 lignes permettent de poser des interrogations sur la grille
# Le "1" correspond au numero de la couche (en l'occurrence il n'y a qu'une couche)
nombre_intervalles = Get number of intervals: 1


for no_intervalle from 1 to nombre_intervalles - 1

	select 'grille'
	phoneme$ = Get label of interval: 1, no_intervalle
	phoneme_suivant$ = Get label of interval: 1, no_intervalle + 1

	if phoneme$ = phoneme1$ and phoneme_suivant$ = phoneme2$

		debut_intervalle1 = Get start time of interval: 1, no_intervalle
		fin_intervalle1 = Get end time of interval: 1, no_intervalle
		debut_intervalle2 = fin_intervalle1
		fin_intervalle2 = Get end time of interval: 1, no_intervalle + 1

		milieu1  = (debut_intervalle1 + fin_intervalle1 ) / 2
		milieu2 = (debut_intervalle2 + fin_intervalle2 ) / 2

#Guillemets simples tjrs faculatitfs

		select 'son'
		diphone = Extract part: 'milieu1', 'milieu2', "rectangular", 1, "no"

	endif
endfor


#printline 'hello'
pause test
