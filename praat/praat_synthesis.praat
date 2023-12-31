# script pour la synthese
#
# 1:18 pour applatissement du Pitch

table = Read Table from tab-separated file: "dico.txt"

nom$ = "faure"
son$ = nom$ + ".wav"
grille$ = nom$ + ".TextGrid"

son = Read from file: son$
intersections = To PointProcess (zeroes): 1, "yes", "no"
grille = Read from file: grille$

phrase_ortho$ = "tsigane vodka parcmètre"
phrase_phon$ = "_"
if right$(phrase_ortho$) != " "
	phrase_ortho$ = phrase_ortho$ + " "
endif

longueur_phrase = length(phrase_orth$)

#on peut aussi aller chopper tous les espaces pour separer ?
while longueur_phrase > 0
	longueur_mot = index(phrase_ortho$, " ") - 1
	mot_ortho$ = left$(phrase_ortho$, longueur_mot)
	@phonetisation
	phrase_phon$ = phrase_phon$ + mot_phonetique$ # + "_"
	phrase_ortho$ = right$(phrase_ortho$, longueur_phrase - (longueur_mot + 1))
	longueur_phrase = length(phrase_ortho$)
endwhile
# rajouter parcmetre dans le dico avec sa transcription phonetiaue paRkmEtR

procedure phonetisation
	select 'table'
	extraction_mot = Extract rows where column (text): "ortho", "is equal to", mot_ortho$
	select 'extraction_mot'
	mot_phonetique$  = Get value: 1, "phonetique"
endproc

procedure modif_f0
	select diphone'i'
	manip = To Manipulation: 0.01, 75, 600
	pitch = Extract pitch tier
	nb_f0_points = Get number of points
	
	if nb_f0_points > 0
		Remove points between: 0, 1
		Add point: 0.01, 210
		select 'manip'
		plus 'pitch'
		Replace pitch tier
		manip = selected("Manipulation")
		pitch = selected("PitchTier")
		select 'manip'
		diphone'i' = Get resynthesis (overlap-add)

		select 'manip'
		plus 'pitch'
		Remove

		select diphone'i'
	endif
endproc

# Le "1" correspond au numero de la couche (en l'occurrence il n'y a qu'une couche)
nombre_intervalles = Get number of intervals: 1

@extraire_tous_les_diphones
@modif_f0
@concatener_diphones


procedure extraire_tous_les_diphones
phrase_phon$ = phrase_phon$ + "_"
longueur_mot = length(phrase_phon$)

	for i from 1 to longueur_mot - 1
		diphone$ = mid$(phrase_phon$, i, 2)
		phoneme1$ = mid$(diphone$, 1, 1)
		phoneme2$ = mid$(diphone$, 2, 1)
		#pause 'phoneme1$' / 'phoneme2$'
		@extraction_du_diphone

	endfor
endproc

procedure extraction_du_diphone

	for no_intervalle from 1 to nombre_intervalles - 1

		select 'grille'
		phoneme$ = Get label of interval: 1, no_intervalle
		phoneme_suivant$ = Get label of interval: 1, no_intervalle + 1

		if phoneme$ = phoneme1$ and phoneme_suivant$ = phoneme2$
			@obtenir_parties_a_extraire
#Guillemets simples tjrs faculatitfs

			select 'son'
			diphone'i' = Extract part: 'debut', 'fin', "rectangular", 1, "no"

		endif
	endfor

endproc

procedure obtenir_parties_a_extraire
	debut_intervalle1 = Get start time of interval: 1, no_intervalle
	fin_intervalle1 = Get end time of interval: 1, no_intervalle
	debut_intervalle2 = fin_intervalle1
	fin_intervalle2 = Get end time of interval: 1, no_intervalle + 1
	
	@obtenir_milieu: debut_intervalle1, fin_intervalle1
	debut = obtenir_milieu.return
	@obtenir_milieu: debut_intervalle2, fin_intervalle2
	fin = obtenir_milieu.return
endproc

procedure obtenir_milieu: .debut_intervalle, .fin_intervalle
	.milieu = (.debut_intervalle + .fin_intervalle) / 2
	@obtenir_intersection_zero: .milieu
	.return = obtenir_intersection_zero.return
endproc

procedure obtenir_intersection_zero: .milieu
	select 'intersections'
	.index_intersection = Get nearest index: .milieu
	.nouveau_milieu = Get time from index: .index_intersection
	.return = .nouveau_milieu
endproc

procedure concatener_diphones
	select diphone1
	for b from 2 to longueur_mot - 1
		plus diphone'b'
	endfor

	Concatenate #with overlap: 0.005
endproc
