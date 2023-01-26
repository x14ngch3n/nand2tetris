DIRS = ArrayTest Square ExpressionLessSquare
JACKFILES = $(shell find . -name *T.xml)

tokenizer:
	$(foreach dir, $(DIRS), ./JackAnalyzer.py $(dir);)

test_tokenizer: tokenizer
	$(foreach file, $(JACKFILES), ../../tools/TextComparer.sh $(file) $(file).1;)

clean:
	$(foreach dir, $(DIRS), rm -rf $(dir)/*.1)
	rm -rf __pycache__