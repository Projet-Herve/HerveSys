import json

class recherche_piece:
	def __init__(self,piece=None,id=None,pieces=None):
		self.piece = piece
		self.id = id
		self.pieces = pieces
		
	def avec_son_id(id):
		if id :
			to_return = None
			for i in pieces :
				if pieces[i]['id'] == id :
					to_return = i
			return to_return
					
	def avec_son_nom(piece):
		if piece :
			try : return pieces[piece]['id']
			except : return False

class recherche_objet:
	def __init__(self,piece=None,id=None,objet=None,pieces=None):
		self.piece = piece
		self.id = id
		self.pieces = pieces
		
	def avec_son_id(piece,id):
		if id and piece:
			for i in pieces[piece]['objets']:
				to_return = None
				if pieces[piece]['objets'][i]['id'] == id :
						to_return = i
				return to_return

	def avec_son_nom(piece,objet):
		if piece and objet:
			try : return pieces[piece]['objets'][objet]['id']
			except : return 'La piece ou l\'objet n\'existe pas'
		else :
			return '[erreur] Le nom de piece ou de l\'objet n\'a pas été renseigne'


# print (recherche_piece.avec_son_id(id=2))
# print (recherche_piece.avec_son_nom(piece='salon'))
# print (recherche_objet.avec_son_id(piece='cusine',id=1))
# print (recherche_objet.avec_son_nom(piece='cusine',objet='lampe'))



