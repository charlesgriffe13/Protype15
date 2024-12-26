import py5

def setup():
    py5.size(400, 200)

def draw():
    py5.background(220)
    py5.rectMode(py5.CENTER)
    py5.rect(py5.width / 2, py5.height / 2, 50, 50)

def keyPressed():
    if py5.key == 'q':
        py5.quit()

py5.run_sketch()
