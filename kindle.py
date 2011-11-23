import shutil, re

# checks that the kindle is plugged in, and finds the notes file
alphabet = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
notes_path = 'C:\Users\Ben\Documents\My Dropbox\Book Notes\\'
kindle_path = ':\documents\My clippings.txt'

success = False
for drive in alphabet:
	try:
		kindle_file = open(drive+kindle_path)
		success = True
	except IOError as e:
		continue

if (success==False):
	print "File not found"
else:
	#stuff we do when we have successfully found the file
	
	#parse the file
	#use reg exs to find the titles of books that have notes/highlights
	#add each new title to a dict, so as you go through the notes file you can check against existing keys in the dict
	#if the key already exists, append the new note to the value. If it doesn't, create a new key-value pair
		
	#open the file (read to string)
	filestr = kindle_file.read()
	
	#define the needed reg ex's
	r_title_and_author = re.compile('.*')
	r_author = re.compile(r'\(([^)]*)\)')
	r_comment = re.compile('.*$')
	r_bookmark = re.compile('Bookmark')
	r_note = re.compile('Note')
	r_highlight = re.compile('Highlight')
	r_location = re.compile('(?<=Loc\.\s)[0-9]+-*[0-9]*')
	r_replace = re.compile('(\:+)|(\\+)')
	r_justremove = re.compile('(\"+)|(\++)|(\?+)|(\|+)')
	# r_page = re.compile('(?<=Page\s)[0-9]+-*[0-9]*')
	# author = r_author.search(filestr).group(1)
	
	#define an empty dictionary
	#holds the name and author of the book as a key
	#value is a string of all the notes in the book
	book_dict = {}
	
	#get a list of all entries in the file by splitting by entrydivider
	entries = re.split('==========\n', filestr, re.DOTALL , re.MULTILINE)
	# this only splits into a max of 17 pieces, on dev machine
	
	#call splitting function recursively. Keep going until it reaches EOF
	eof = False
	while (eof==False):
		entries2 = re.split('==========\n', entries[len(entries)-1], re.DOTALL , re.MULTILINE)
		for entry in entries2:
			if (entry==""):
				#at the end of the file, there is nothing for re.split to do, and it returns an empty string
				eof = True
			else:
				entries.append(entry)
			
	#then, split each entry by line
	for entry in entries:
		lines = re.split('\n', entry, re.DOTALL, re.MULTILINE)
		try:
			#ensures we have the right document format/we have started parsing in the right place
			titleandauthor = lines[0]
			details = lines[1]
			content = lines[3]
		except IndexError:
			print "Error Ocurred!\n"
			continue
		finally:
			#Don't need to do parsing within the lines atm. SO its all commented out. But, it might be useful later
			#apply the author pattern, searching from the end of the title & author string - get author
			# title = re.split(r_author, titleandauthor)[0]
			# author = re.split(r_author, titleandauthor)[1]
			
			#parse details, to get whether its Bookmark/Note/Highlight, its location, and the time it was made
			
			#type_dict = {'Bookmark':r_bookmark, 'Note':r_note, 'Highlight':r_highlight }
			#for name, pattern in type_dict.iteritems():
			#	try:
			#		pattern.search(details).group()
			#	except AttributeError as e:
			#		a = type
			#	finally:
			#		type = name
				
			# location = r_location.search(details).group()
			#posible also to parse the page information/date
			#add some time later?

			try:
				initial_entry = book_dict[titleandauthor]
			except KeyError:
				initial_entry = titleandauthor + '\n\n'
			book_dict[titleandauthor] = initial_entry +'\n'+ details +'\n'+ content +'\n'
			out = book_dict[titleandauthor]
		
	for key, value in book_dict.iteritems():
		
		#just use the title as filename
		filename = re.split(r_author, key)[0]
		
		#remove any characters that can't be printed to a filename
		safe_name=False
		while (safe_name==False):
			filename_safe = filename
			
			new_filename = re.sub(r_replace, ' -', filename)
			new_filename = re.sub(r_justremove, '', new_filename)
			if (new_filename==filename):
				safe_name = True
			else:
				filename = new_filename
		
		
		print filename + "\n"	
		f = open(notes_path+filename+'.txt', 'w')
		f.write(value)
		f.close()
	
