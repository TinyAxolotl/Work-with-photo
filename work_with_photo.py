import abc
import random
from PIL import Image, ImageDraw, ImageFilter
import glob, os

mode = 0
flag_exception = 0

print('''
Режимы.  
1. - Серый  
2. - Негатив  
3. - Не трогать -- Для бота 
4. - Сепия 
5. - Шумы 
6. - Осветление\затемнение 
7. - Ч\Б 
8. - Изменение размера


''')
while flag_exception != 1:
	try:
		mode = int(input('Режим:')) 
		while mode > 9:
			mode = int(input('Режим:'))
	#2284064--428125
		extension = input('Расширение файла: ')
		f = input('Название файла: ') + extension
		s = input('Сохранить как: ') + extension
	except Exception:
		print('Что-то не так. Режим нужно выбирать цифрами. Расширение файла: .png, .jpg и т.д. ')
		flag_exception = 0
	else:
		image = Image.open(f) 
		draw = ImageDraw.Draw(image) 
		width = image.size[0] #ширина 
		height = image.size[1] #высота 	
		pix = image.load()

		#f = open('123.jpeg', 'rb')
		#a = f.read()
		#f.close()

		if (mode == 1):
			#print("Оттенки серого")
			for i in range(width):
				for j in range(height):
					a = pix[i, j][0]
					b = pix[i, j][1]
					c = pix[i, j][2]
					S = (a + b + c) // 3
					draw.point((i, j), (S, S, S))

		if (mode == 2):
			# Негатив.
			for i in range(width):
				for j in range(height):
					a = pix[i, j][0]
					b = pix[i, j][1]
					c = pix[i, j][2]
					draw.point((i, j), (255 - a, 255 - b, 255 - c))

		if (mode == 3):
			massiv=[0,0,0]
			for i in range(width):
				for j in range(height):
					massiv.append(pix[i,j][0])
					massiv.append(pix[i,j][1])
					massiv.append(pix[i,j][2])
					# Первый вариант вывода массива значений пикселей
					# Пытаюсь достать значения каждого байта цвета по отдельности
			'''f = open('test0.txt', 'w')
			f.write(str(massiv))
			f.close'''
			

			# Здесь в массив вводится массив байтов каждого пикселя. Вроде так поудобнее, хз.
			# Скорее всего будет основным методом работы с ИЗО.
			# Изучить возможности image.histogram. Должно выводить гистограмму с количеством разных пикселей.
			# Таким образом можно определить фон, буквы и отфильтровать шум (???)

			massiv = [0]
			for i in range(width):
				for j in range(height):
					a = image.getpixel((i, j))
					massiv.append(a)
				massiv.append('\n')
			f = open('test1.txt', 'w')
			f.write(str(massiv))
			f.close

		if (mode == 4):
			depth = int(input('Интенсивность:'))
			for i in range(width):
				for j in range(height):
					a = pix[i, j][0]
					b = pix[i, j][1]
					c = pix[i, j][2]
					S = (a + b + c) // 3
					a = S + depth * 2
					b = S + depth
					c = S
					if (a > 255):
						a = 255
					if (b > 255):
						b = 255
					if (c > 255):
						c = 255
					draw.point((i, j), (a, b, c))
			
		if (mode == 5):
			depth = int(input('Интенсивность:'))
			for i in range(width):
				for j in range(height):
					rand = random.randint(-depth, depth)
					a = pix[i, j][0] + rand
					b = pix[i, j][1] + rand
					c = pix[i, j][2] + rand
					if (a < 0):
						a = 0
					if (b < 0):
						b = 0
					if (c < 0):
						c = 0
					if (a > 255):
						a = 255
					if (b > 255):
						b = 255
					if (c > 255):
						c = 255
					draw.point((i, j), (a, b, c))

		if (mode == 6):
			depth = int(input('Интенсивность:'))
			for i in range(width):
				for j in range(height):
					a = pix[i, j][0] + depth
					b = pix[i, j][1] + depth
					c = pix[i, j][2] + depth
					if (a < 0):
						a = 0
					if (b < 0):
						b = 0
					if (c < 0):
						c = 0
					if (a > 255):
						a = 255
					if (b > 255):
						b = 255
					if (c > 255):
						c = 255
					draw.point((i, j), (a, b, c))
			
		if (mode == 7):
			depth = int(input('Интенсивность:'))
			for i in range(width):
				for j in range(height):
					a = pix[i, j][0]
					b = pix[i, j][1]
					c = pix[i, j][2]
					S = a + b + c
					if (S > (((255 + depth) // 2) * 3)):
						a, b, c = 255, 255, 255
					else:
						a, b, c = 0, 0, 0
					draw.point((i, j), (a, b, c))

		if (mode == 8):
			resize_mode = int(input('''
			Методы ресайза: 
			1. - Nearest neighbor
			2. - Convolution (LANCZOS)
			3. - Bilinear
			4. - Bicubic
			'''))
			while resize_mode > 4:
				resize_mode = int(input())
			resolution = (input('Необходимое разрешение (вводить, например, 1920х1080. т.е. без пробела и с иксом между цифрами):'))
			resolution.upper()
			resolution = resolution.split('x')
			resolution = [int(resolution[0]), int(resolution[1])]
			if (resize_mode == 1):
				image.thumbnail(resolution, Image.NEAREST)
			if (resize_mode == 2):
				image.thumbnail(resolution, Image.LANCZOS)
			if (resize_mode == 3):
				image.thumbnail(resolution, Image.BILINEAR)
			if (resize_mode == 4):
				image.thumbnail(resolution, Image.BICUBIC)

		print('Дело сделано!')
		image.save(s, "JPEG")
		del draw
		flag_exception = 1 
		input()
		input()











































'''
f = open('mass.txt', 'w')
f.write(pix)
f.close()

'''

'''a = ''
a = str(a)

class Storage:

    @abc.abstractclassmethod
    def read (self, name):
        pass
    
    def write (self, name, text):
        self.s = ''
        pass

class FileStorageBytes(Storage):
    def write(self, name, text):
        f = open(name, 'wb')
        f.write('text')
        f.close()
    pass

    def read(self, name):
        f = open(name, 'rb')
        pass

f = FileStorageBytes()
a = f.read('123.jpeg')
f.write('test.txt', a)'''
