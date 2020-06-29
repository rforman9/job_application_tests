#! /usr/bin/python

# renumber.py version2.0
# file sequence renumber utility
# Richard Forman
# 27 Jun 2020

import os,sys,re
from argparse import ArgumentParser

#####================ Defines =========================####
VALIDEXT = ["jpg", "png", "tif", "tga", "exr", "dpx"] #add the file extensions for the types of file you want to renumber here


#####=============== Functions ========================#####
def getCLI():  #parses options passed
	parser = ArgumentParser(description="Rename image sequences in supplied path")
	parser.add_argument("filepath", type= str, help="path where files to be renamed are stored")
	parser.add_argument("-s", "--startFrame", dest="startFrame", help="specifies the start frame and padding renamed files will start with this number, i.e. 0101")
	parser.add_argument("-d", "--dryrun", action="store_true", dest="dryrun", default=False, help="simulate the script but make no real changes to the filesystem")
	return parser.parse_args( args )

def sortListByDigits(_fileList=None): 	# this function is Mark Byers python variation of Jeff Atwood's 
	if _fileList:						# natural sort. So I can't take full credit for it unfortunatlely.
		convert = lambda text: int(text) if text.isdigit() else text
		alphanum_key = lambda key: [convert(c) for c in re.split("([0-9]+)", key)]
    	return sorted(_fileList, key = alphanum_key)

def renum(_path=None, _dryrun=None, _startFrame=None, _padding=None):  # this function renumbers the files in the directory that is passed to it
	
	basenames=list()
	extensions=list()
	newFiledict=dict()
	if not _startFrame: _startFrame = 0
	#get list of image files in filepath
	filelist = [filename for filename in os.listdir(_path) if filename.split(".")[-1] in VALIDEXT]
	filelist = sortListByDigits(_fileList=filelist)

	#get basenames and extensions
	for filename in filelist:
		if filename.split(".")[0] not in basenames:
			basenames.append(filename.split(".")[0])
		if filename.split(".")[-1] not in extensions:
			extensions.append(filename.split(".")[-1])

	#split list on basename ext combo
	for basename in basenames:
		for extension in extensions:
			name_ext=".".join([basename,extension])
			for filename in filelist:
				validFile=basename in filename and extension in filename
				if validFile and name_ext not in newFiledict:
					newFiledict[name_ext]=[filename,]
				elif validFile and name_ext in newFiledict:
					newFiledict[name_ext].append(filename)

	print "renumbering:"
	for k,v in newFiledict.iteritems():
		for x in range ( len(v)):
			src="{}{}".format(_path,v[x])
			dest="{}{}".format(_path,"{}.{}.{}".format(k.split(".")[0],str(x+_startFrame).zfill(_padding),k.split(".")[1]))
			print " {} to {}".format(src,dest)
			if not _dryrun:
				os.rename(src,dest)

	if _dryrun:
		print "dryrun mode, no filenames actually changed"
	else:
		print "image file sequences have been renumbered"

#####====================== MAIN ========================#####

def main( args ):

	args = getCLI()

	path 		= 	args.filepath
	dryrun 		= 	args.dryrun
	startFrame 	= 	args.startFrame

	if path and not os.path.exists(path):
		raise Exception ("supplied path does not exist")
		return(-1)

	#make sure path has trailing slash
	if path and not path.endswith(os.path.sep):
		path += os.path.sep

	if startFrame and startFrame.isdigit():
		destPadding = len(startFrame)
		print "padding = ",destPadding
		startFrame = int(startFrame.lstrip("0"))
	else:
		startFrame = 1
		destPadding = 2
	
	try:
		renum(_path=path,_dryrun=dryrun, _startFrame=startFrame, _padding=destPadding)
	except Exception, e:
		raise e
		return(-1)
	return(0)

#####======= For Option testing and easy re-use ========##### 

if __name__ == "__main__":
	args = sys.argv[1:]
	
	# args += [
	# 	"O:/renametest/",
	# 	"--startFrame", "001",
	# 	"--dryrun",
	# 	# "-h",
		
	# ]

	sys.exit( main( args ) );