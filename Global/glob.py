global mm

def generarmem():
    mm = mmap.mmap(-1, 90000)

def cargarmem(thetas):
    mm.write(thetas)

def leermem():
    return mm.readline()
