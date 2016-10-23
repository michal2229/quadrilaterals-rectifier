interpreter=python2
mainfile=find_rect_and_transform.py

all: hello

hello: *.py
	$(interpreter) $(mainfile) ./input/* ./output/

