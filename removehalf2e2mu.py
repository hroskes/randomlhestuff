import os

#doremovehalf2e2mu = False
#newscale = "6.2500000E+01"

doremovehalf2e2mu = True
newscale = "3.7500000E+02"

def removehalf2e2mu(*files):
    if newscale:
        print "Warning: changing the scale!"
    total4l = 0
    total2e2mu = 0
    totalnwritten2e2mu = 0

    for filename in files:
        eventcounter4l = 0
        eventcounter2e2mu = 0
        nwritten2e2mu = 0
        print filename + ":"
        newfilename = filename.replace(".lhe", "_fixscale.lhe")
        if newfilename == filename:
            raise ValueError("Don't overwrite the old file!")
        if os.path.exists(newfilename) or "_fixscale.lhe" in filename:
            continue

        with open(filename) as f, open(newfilename, "w") as newf:
            thisevent = ""
            inevent = False
            lineinevent = 0
            for line in f:
                if "<event>" in line:
                    newf.write(thisevent)
                    thisevent = ""
                    inevent = True
                    lineinevent = 0
                    electrons = 0
                    muons = 0

                if inevent:
                    data = line.split()
                    if lineinevent == 1:
                        if newscale:
                            scalestr = data[3]
                            line = line.replace(scalestr, newscale)

                thisevent += line
                lineinevent += 1

                if "</event>" in line:
                    inevent = False
                    if electrons == 4 or muons == 4:
                        eventcounter4l += 1
                        writethisevent = True
                    elif electrons == 2 and muons == 2:
                        eventcounter2e2mu += 1
                        writethisevent = not doremovehalf2e2mu or bool((total2e2mu + eventcounter2e2mu) % 2)
                        nwritten2e2mu += writethisevent
                    else:
                        raise ValueError("electrons=%i, muons=%i" % (electrons, muons))
                    if writethisevent:
                        newf.write(thisevent)
                    thisevent = ""

                if inevent:
                    try:
                        id = int(data[0])
                        if abs(id) == 11:
                            electrons += 1
                        if abs(id) == 13:
                            muons += 1
                    except ValueError:
                        pass

            newf.write(thisevent)

            total2e2mu += eventcounter2e2mu
            total4l += eventcounter4l
            totalnwritten2e2mu += nwritten2e2mu

            print "    2e2mu: %i --> %i" % (eventcounter2e2mu, nwritten2e2mu)
            print "       4l: %i --> %i" % (eventcounter4l, eventcounter4l)

    print "Total:"
    print "    2e2mu: %i --> %i" % (total2e2mu, totalnwritten2e2mu)
    print "       4l: %i --> %i" % (total4l, total4l)

if __name__ == "__main__":
    import sys
    removehalf2e2mu(*sys.argv[1:])
