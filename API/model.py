# import peewee

# db = peewee.SqliteDatabase('database.db')

# class Ar_Condicionado(peewee.Model):
# 	device_id = peewee.PrimaryKeyField
# 	temperatura = peewee.TextField

# 	def to_dict(self):
# 		return({'id':self.id, 'temperatura':self.temperatura})

# 	class Meta:
# 		database = db

# class Termometro(peewee.Model):
# 	device_id = peewee.PrimaryKeyField
# 	temperatura = peewee.TextField

# 	def to_dict(self):
# 		return({'id':self.id, 'temperatura':self.temperatura})

# 	class Meta:
# 		database = db

# class Fechadura(peewee.Model):
# 	device_id = peewee.PrimaryKeyField
# 	status = peewee.TextField
	
# 	def to_dict(self):
# 		return({'id':self.id, 'status':self.status})

# 	class Meta:
# 		database = db

# class Lampada(peewee.Model):
# 	device_id = peewee.PrimaryKeyField
# 	status = peewee.TextField

# 	def to_dict(self):
# 		return({'id':self.id, 'status':self.status})

# 	class Meta:
# 		database = db
