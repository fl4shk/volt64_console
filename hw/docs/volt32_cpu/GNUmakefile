PROJECT=$(shell basename $(CURDIR))

build/${PROJECT}.pdf: build/${PROJECT}.bbl
	lualatex --output-directory=build ${PROJECT}
	cp build/${PROJECT}.pdf .

build/${PROJECT}.bbl: build/${PROJECT}.bcf
	biber build/${PROJECT}

build/${PROJECT}.bcf: ${PROJECT}.tex
	mkdir -p build
	lualatex --output-directory=build ${PROJECT}

build/${PROJECT}.rtf: build/${PROJECT}.pdf
	latex2rtf ${PROJECT}.tex
	cp ${PROJECT}.rtf build

clean:
	rm -f build/*
