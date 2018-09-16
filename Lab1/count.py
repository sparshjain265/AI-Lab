#Take the input (file name) and open the file
print("Enter file name: ")
fileName = str(input())
f = open(fileName, 'r')
#Initialize the number of words and mode of reading
words = 0
mode = 0	#mode 0 means we are reading a whitespace, 1 means we are reading a word
ch = f.read(1)	#read character by character
while(ch != '') :	#if a character is read
	#if we were reading whitespaces and a character comes, increment word and change mode
	if(mode == 0 and ch != ' ' and ch != '\t' and ch != '\n') :
		words += 1
		mode = 1
	#if we were reading characters and a whitespace comes, change mode
	elif(mode == 1 and (ch == ' ' or ch == '\t' or ch == '\n')) :
		mode = 0
	#read next character
	ch = f.read(1)
#close the file
f.close()

#print the output
print("Words = " + str(words))

