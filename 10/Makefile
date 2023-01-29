DIRS = ArrayTest Square ExpressionLessSquare
XMLTFILES = $(shell find . -name *T.xml)
XMLFILES = $(shell find . -name *[^T].xml)

analyzer:
	$(foreach dir, $(DIRS), ./JackAnalyzer.py $(dir);)

test_tokenizer: analyzer
	$(foreach file, $(XMLTFILES), ../../tools/TextComparer.sh $(file) $(file).1;)

test_compilation: analyzer
	$(foreach file, $(XMLFILES), ../../tools/TextComparer.sh $(file) $(file).1;)

clean:
	$(foreach dir, $(DIRS), rm -rf $(dir)/*.1)
	rm -rf __pycache__