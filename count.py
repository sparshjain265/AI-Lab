print("Enter file name: ")
fileName = str(input())
f = open(fileName, 'r')
words = 0
mode = 0
ch = f.read(1)
while(ch != '') :
	if(mode == 0 and ch != ' ' and ch != '\t' and ch != '\n') :
		words += 1
		mode = 1
	elif(mode == 1 and (ch == ' ' or ch == '\t' or ch == '\n')) :
		mode = 0
	ch = f.read(1)
f.close()
print("Words = " + str(words))

