.PHONY: statement

statement: statement/index.pdf

statement/index.pdf: statement/index.md $(wildcard statement/*.jpg statement/*.png) problem.json subtasks.json ../template.tex
	tps statement
