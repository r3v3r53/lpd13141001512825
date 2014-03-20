from reportlab.pdfgen import canvas
def hello(c):
	c.drawString(100,100,"Hello world")

def cursormoves1(canvas):
	from reportlab.lib.units import inch
	texto = ('linha 1', 'linha 2','linha 3','linha 4','linha 5')
	textobject = canvas.beginText()
	textobject.setTextOrigin(inch, 10 * inch)
	textobject.setFont("Helvetica-Oblique", 14)
	
	#for line in file('texto.txt','r'):
	for line in texto:
		textobject.textLine(line)
	textobject.setFillGray(0.4)
	textobject.textLines('''
	texto de exemplo paraescrever no documento pdf
	nova linha
	''')
	canvas.drawText(textobject)
	
c = canvas.Canvas("hello.pdf")
#hello(c)
cursormoves1(c)
c.showPage()
c.save()
