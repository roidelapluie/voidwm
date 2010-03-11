def getDesk(w,c,s):
	cclass = w.get_wm_class()
	if 'Conky' in cclass:
		return -1
	if 'Firefox' in cclass:
		return 1
	if 'sakura' in cclass and not s.popup:
		return 'p'
	return None
	

def getLayout(n, p):
	ssw = 1180
	ssh = 800
	pos = []
	if p == 0:
		layoutCols = [3,2]
		effective  = [0,0]
		defsize = 4
		i = 0
		curCol = 0
		while i < n:
			if effective[curCol] == layoutCols[curCol]:
				curCol += 1
			if len(effective) == curCol:
				effective.append(0)
				layoutCols.append(defsize)
			effective[curCol] += 1
			i += 1
		for i in xrange(0, effective.count(0)):
			effective.remove(0)
		if len(effective) == 0:
			return None
		width = 1180/len(effective)
		decal = ssw - width*len(effective)
		col = 0
		for c in effective:
			height = ssh/c
			decalh = ssh - c*height
			for s in xrange(0, c):
				w = width
				h = height
				if col+1 == len(effective):
					w += decal
				if w+1 == c:
					h += decalh
				alignx = col*width
				aligny = s*height
				pos.append((alignx, aligny, w-2, h-2))
			col +=1
	elif p == 4:
		layoutCols = [1,2,2,1]
		effective  = [0,0]
		defsize = 3
		i = 0
		curCol = 0
		while i < n:
			if effective[curCol] == layoutCols[curCol]:
				curCol += 1
			if len(effective) == curCol:
				effective.append(0)
				layoutCols.append(defsize)
			effective[curCol] += 1
			i += 1
		for i in xrange(0, effective.count(0)):
			effective.remove(0)
		if len(effective) == 0:
			return None
		height = 800/len(effective)
		decalh = ssh - height*len(effective)
		col = 0
		for c in effective:
			width = ssw/c
			decal = ssw - c*width
			for s in xrange(0, c):
				w = width
				h = height
				if col+1 == len(effective):
					h += decalh
				if w+1 == c:
					w += decal
				aligny = col*height
				alignx = s*width
				pos.append((alignx, aligny, w-2, h-2))
			col+=1
	elif p == 1:
		i = 0
		width = ssw - 15*(n-1)
		height = ssh - 15*(n-1)
		while i < n:
			pos.append((i*15, i*15, width-2, height-2))
			i+=1
	elif p == 2:
		i = 0
		width = ssw - 15*(n-1)
		height = ssh - 15*(n-1)
		while i < n:
			pos.append(((n-i-1)*15, (n-i-1)*15, width-2, height-2))
			i+=1
	elif p == 3:
		i = 0
		width = ssw + 102
		height = ssh + 2
		while i < n:
			pos.append((-1, -1, width, height))
			i+=1
	return pos

def fixit(client, window):
	cclass = window.get_wm_class()
		#client.deiconify()
		#client.tilesize = {'x':0, 'y': 1180, 'width': 100, 'height':800}
		#client.moveresize(0,1180,100,800, True)

for i in range (1,7):
	getLayout(i,4)
