def removehalf2e2mu(*files):
    total4l = 0
    total2e2mu = 0

    for filename in files:
        eventcounter4l = 0
        eventcounter2e2mu = 0
        print filename + ":"
        newfilename = filename.replace(".lhe", "half2e2mu.lhe")
        if newfilename == filename:
            raise ValueError("Don't overwrite the old file!")

        with open(filename) as f, open(newfilename, "w") as newf:
            thisevent = ""
            inevent = False
            for line in f:
                if "<event>" in line:
                    newf.write(thisevent)
                    thisevent = ""
                    inevent = True
                    electrons = 0
                    muons = 0

                thisevent += line

                if "</event>" in line:
                    inevent = False
                    if electrons == 4 or muons == 4:
                        eventcounter4l += 1
                        writethisevent = True
                    elif electrons == 2 and muons == 2:
                        eventcounter2e2mu += 1
                        writethisevent = bool((total2e2mu + eventcounter2e2mu) % 2)
                        nwritten2e2mu += writethisevent
                    else:
                        raise ValueError("electrons=%i, muons=%i" % (electrons, muons))
                    if writethisevent:
                        newf.write(thisevent)
                    thisevent = ""

                if inevent:
                    try:
                        data = line.split()
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

            print "    2e2mu: %i --> %i" % (eventcounter2e2mu, nwritten2e2mu)
            print "       4l: %i --> %i" % (eventcounter4l, eventcounter4l)

if __name__ == "__main__":
    import sys
    removehalf2e2mu(*sys.argv[1:])
