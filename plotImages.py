from PIL import Image
from collections import defaultdict
import time
from kdtree import KDTree


def nearestNeighbours(data , point , k):
	distances = []
	tmp = []

	start = time.mktime(time.localtime())
	for i in range(0 , len(data)):
		distances.append(distance(data[i] , point))
		tmp.append(i)

	end = time.mktime(time.localtime())
	print str(end - start) + ' secs to get distances'
	start = time.mktime(time.localtime())

	tmp.sort(key = lambda x : distances[x])

	end = time.mktime(time.localtime())
	print str(end - start) + ' secs to sort'
	start = time.mktime(time.localtime())

	return tmp[0:k]


def knn():
	f = open('train.csv' , 'r')
	data = [] # all labeled data
	lookupTable = dict()
	num = 0
	for line in f:
		d = line.split(',')
		if d[0] == 'label':
			continue
		d = map(int , d)
		data.append(d)
		lookupTable[tuple(d[1:])] = d[0]
		if num > 40000:
			break
		num += 1

	f.close()

	points1 = map(lambda x : tuple(x[1:]) , data)
	tree = KDTree.construct_from_data(points1)

	num = 0

	points = map(lambda x : x[1:] , data)

	f = open('train.csv' , 'r')
	for line in f:
		num += 1
		if num < 32000:
			continue
		if num > 32100:
			break

		d = line.split(',')
		if d[0] == 'label':
			continue
		d = map(int , d)
		start = time.mktime(time.localtime())
		nn = tree.query(tuple(d[1:]) , 10)

		end = time.mktime(time.localtime())
		#print str(end - start) + ' secs to get distances'
		start = time.mktime(time.localtime())
		#nn = nearestNeighbours(points , d[1:] , 10)
		counts = defaultdict(int)
		for x in nn:
			counts[lookupTable[x]] += 1

		print str(d[0] == sorted(counts , key = lambda x : counts[x] , reverse = True)[0])


	f.close()

def distance(a , b):
	c = 0
	exponent = 1.0
	for i in range(0 , len(a)):
		c += abs(pow((a[i] - b[i]) , exponent))

	c = 1.0*c/len(a)
	c = pow(c , 1/exponent)
	return c


def plotAndShow(image):
	im = Image.new('L' , (28 , 28))
	for i in range(1 , len(image)):
		x = (i - 1)%28
		y = (i - 1)/28
		im.putpixel(( x , y) , image[i])
	im.show()

def diffAndShow(a , b):
	c = map(lambda i : abs(a[i] - b[i]) , range(0 , len(a)))
	plotAndShow(c)

def prettyPrint(image):
	for i in range(1 , len(image) , 28):
		print ' '.join(map(str , image[i:i + 28]))
		print '\n'

def test():
	# load model
	f = open('model.csv' , 'r')
	model = []
	for i  in range(0 , 10):
		model.append(0)
	for line in f:
		tmp = line.split(',')
		digit = int(tmp[0])
		model[digit] = map(lambda x : round(float(x), 0), tmp[1:])
		plotAndShow(model[digit])
		#prettyPrint(model[digit])

	f.close()

	exit()

	f = open('train.csv' , 'r')
	n = 0
	for line in f:
		tmp = line.split(',')
		if tmp[0] != 'label':
			n += 1
			label = int(tmp[0])
			image = map(float, tmp[1:])
			least = 10000
			best = None
			for digit in range(0 , len(model)):
				dist = distance(model[digit] , image)
				#print dist
				if dist < least:
					least = dist
					best = digit

			#print str(best) + '\t' + str(label) 
			if best != label:
				print 'best : ' + str(best)
				print 'actual: ' + str(label)
				#plotAndShow(image)
				#plotAndShow(model[best])
				#plotAndShow(model[label])
				#diffAndShow(image , model[label])
				diffAndShow(image , model[best])
				break
				#prettyPrint(image)
				d1 = distance(model[best] , image)

				d2 = distance(model[label] , image)
				#print round(abs(d1 - d2) , 0)
				#print 'dist b/w model digits: ' + str(distance(model[label] , model[best]))

		if n > 1000:
			break


	f.close()

def train():
	f = open('train.csv' , 'r')

	k = []
	for i  in range(0 , 10):
		k.append([])

	for line in f:
		data = line.split(',')
		if data[0] == 'label':
			continue
		data[0] = int(data[0])
		k[data[0]].append(map(int , data[1:]))


	for digit in range(0 , len(k)):
		avg = []
		for i in range(0 , len(k[digit][0])):
			avg.append(0)

		for d in k[digit]:
			for i in range(0 , len(d)):
				avg[i] += d[i]

		for i in range(0 , len(avg)):
			avg[i] = 1.0*avg[i]/len(k[digit])

		print str(digit) + ',' + ','.join(map(str , avg))

	f.close()

if __name__ == '__main__':
	#train()
	#test()
	knn()
