import sys

from struct import *

#
#Se utiliza así:
#
#from parser_stl import STL_Object
#
#stl = STL_Object("archivo_entrada.stl")
#
#stl.make_new_z_axis('x') # "rota" la geometria. El antiguo eje x, pasa a ser el Z
#
#altura = stl.align_to_origin() #alinea al origen
#
#stl.export_to_binary_file("arhivo_salida.stl") #guarda el stl modificado en el archivo
#

class BinaryStream:
    def __init__(self, base_stream):
        self.base_stream = base_stream

    def readByte(self):
        return self.base_stream.read(1)

    def readBytes(self, length):
        return self.base_stream.read(length)

    def readChar(self):
        return self.unpack('b')

    def readUChar(self):
        return self.unpack('B')

    def readBool(self):
        return self.unpack('?')

    def readInt16(self):
        return self.unpack('h', 2)

    def readUInt16(self):
        return self.unpack('H', 2)

    def readInt32(self):
        return self.unpack('i', 4)

    def readUInt32(self):
        return self.unpack('I', 4)

    def readInt64(self):
        return self.unpack('q', 8)

    def readUInt64(self):
        return self.unpack('Q', 8)

    def readFloat(self):
        return self.unpack('f', 4)

    def readDouble(self):
        return self.unpack('d', 8)

    def readString(self):
        length = self.readUInt16()
        return self.unpack(str(length) + 's', length)

    def writeBytes(self, value):
        self.base_stream.write(value)

    def writeChar(self, value):
        self.pack('c', value)

    def writeUChar(self, value):
        self.pack('C', value)

    def writeBool(self, value):
        self.pack('?', value)

    def writeInt16(self, value):
        self.pack('h', value)

    def writeUInt16(self, value):
        self.pack('H', value)

    def writeInt32(self, value):
        self.pack('i', value)

    def writeUInt32(self, value):
        self.pack('I', value)

    def writeInt64(self, value):
        self.pack('q', value)

    def writeUInt64(self, value):
        self.pack('Q', value)

    def writeFloat(self, value):
        self.pack('f', value)

    def writeDouble(self, value):
        self.pack('d', value)

    def writeString(self, value):
        length = len(value)
        self.writeUInt16(length)
        self.pack(str(length) + 's', value)

    def pack(self, fmt, data):
        return self.writeBytes(pack(fmt, data))

    def unpack(self, fmt, length = 1):
        return unpack(fmt, self.readBytes(length))[0]



class Vector:
	def __init__(self):
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
		
	def set(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
	
	def to_string(self):
		return "("+str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"
		
class Cara:
	def __init__(self):
		self.normal = Vector()
		self.vertices = [Vector(),Vector(), Vector()]
		self.atributos = 0

class STL_Object:
	#Cara la geometría a partir del archivo de entrada stl especificado en stl_file
	def __init__(self, stl_file):
		self.stl_file = stl_file
		
		f = open(stl_file, "r")
		stream = BinaryStream(f)
		
		self.file_header = stream.readBytes(80)
		self.n_caras = stream.readInt32()
		self.caras = []
		
		for i in range(0, self.n_caras):
			normal_x = stream.readFloat()
			normal_y = stream.readFloat()
			normal_z = stream.readFloat()
			cara = Cara()
			cara.normal.set(normal_x, normal_y, normal_z)
			for j in range(0, 3):
				x = stream.readFloat()
				y = stream.readFloat()
				z = stream.readFloat()
				cara.vertices[j].set(x, y, z)
			cara.atributos = stream.readUInt16()
			self.caras.append(cara)
		f.close()
	
	#guarda la geometría en el archivo salida stl entregado en out_stl_file
	def export_to_binary_file(self, out_stl_file):
		f = open(out_stl_file, "w")
		stream = BinaryStream(f)
		stream.writeBytes(self.file_header)
		stream.writeInt32(self.n_caras)
		for i in range(0, self.n_caras):
			stream.writeFloat(self.caras[i].normal.x)
			stream.writeFloat(self.caras[i].normal.y)
			stream.writeFloat(self.caras[i].normal.z)
			for j in range(0, 3):
				stream.writeFloat(self.caras[i].vertices[j].x)
				stream.writeFloat(self.caras[i].vertices[j].y)
				stream.writeFloat(self.caras[i].vertices[j].z)
			stream.writeUInt16(self.caras[i].atributos)
		f.close()
		
	#especifica el eje vertical en old_axis. Este será el nuevo eje Z.
	def make_new_z_axis(self, old_axis):
		if old_axis=='x' or old_axis=='X':
			#x->z, z->y, y->x
			for i in range(0, self.n_caras):
				for j in range(0, 3):
					aux_x = self.caras[i].vertices[j].x
					self.caras[i].vertices[j].x = self.caras[i].vertices[j].y
					self.caras[i].vertices[j].y = self.caras[i].vertices[j].z
					self.caras[i].vertices[j].z = aux_x
		elif old_axis=='y' or old_axis=='Y':
			#y->z, z->x, x->y
			for i in range(0, self.n_caras):
				for j in range(0, 3):
					aux_y = self.caras[i].vertices[j].y
					self.caras[i].vertices[j].y = self.caras[i].vertices[j].x
					self.caras[i].vertices[j].x = self.caras[i].vertices[j].z
					self.caras[i].vertices[j].z = aux_y
		elif old_axis=='z' or old_axis=='Z':
			return
	
	#alinea la geometria con el origen, y retorna la altura (eje z)
	def align_to_origin(self):
		if self.n_caras < 1:
			return 0.0
		minimum =  self.caras[0].vertices[0]
		maximum = self.caras[0].vertices[0]
		for i in range(0, self.n_caras):
			for j in range(0, 3):
				if self.caras[i].vertices[j].x < minimum.x:
					minimum.x = self.caras[i].vertices[j].x
				elif self.caras[i].vertices[j].x > maximum.x:
					maximum.x = self.caras[i].vertices[j].x
				if self.caras[i].vertices[j].y < minimum.y:
					minimum.y = self.caras[i].vertices[j].y
				elif self.caras[i].vertices[j].y > maximum.y:
					maximum.y = self.caras[i].vertices[j].y
				if self.caras[i].vertices[j].z < minimum.z:
					minimum.z = self.caras[i].vertices[j].z
				elif self.caras[i].vertices[j].z > maximum.z:
					maximum.z = self.caras[i].vertices[j].z
		center = Vector()
		center.set(maximum.x+minimum.x, maximum.y+minimum.y,maximum.z+minimum.z)
		center.x = float(center.x) / 2.0
		center.y = float(center.y) / 2.0
		center.z = float(center.z) / 2.0
		for i in range(0, self.n_caras):
			for j in range(0, 3):
				self.caras[i].vertices[j].x = self.caras[i].vertices[j].x - center.x
				self.caras[i].vertices[j].y = self.caras[i].vertices[j].y - center.y
				self.caras[i].vertices[j].z = self.caras[i].vertices[j].z - minimum.z #este no queda centrado, queda sobre el origen
		return maximum.z-minimum.z


#def main():
#	stl_file = ""
#	if len(sys.argv) < 2:
#		print "Error numero de argumentos"
#		return
#	stl_file = sys.argv[1] #lo saco de la linea de comandos
#	print "Archivo leido de argumentos: " + stl_file
#	
#	stl = STL_Object(stl_file)
#	stl.make_new_z_axis('x')
#	altura = stl.align_to_origin()
#	stl.export_to_binary_file("nuevostl.stl")
#	
#main()
