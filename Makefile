nothing:

merge-pdfs: pro/attachments/problem.pdf

pro/attachments/problem.pdf: pro/statement/index.pdf
	mkdir -p pro/attachments
	pdfunite pro/statement/index.pdf pro/attachments/problem.pdf
