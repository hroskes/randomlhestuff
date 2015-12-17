def printleptonfractions(*files):
    total2e2mu = 0
    total4mu = 0
    total4e = 0

    for filename in files:
        eventcounter4e = 0
        eventcounter4mu = 0
        eventcounter2e2mu = 0
        print filename + ":"

        with open(filename) as f:
            inevent = False
            lineinevent = 0
            for line in f:
                if "<event>" in line:
                    inevent = True
                    lineinevent = 0
                    electrons = 0
                    muons = 0

                lineinevent += 1

                if "</event>" in line:
                    inevent = False
                    if electrons == 4:
                        eventcounter4e += 1
                    elif muons == 4:
                        eventcounter4mu += 1
                    elif electrons == 2 and muons == 2:
                        eventcounter2e2mu += 1
                    #else:
                    #    raise ValueError("electrons=%i, muons=%i" % (electrons, muons))

                if inevent:
                    data = line.split()
                    try:
                        id = int(data[0])
                        if abs(id) == 11:
                            electrons += 1
                        if abs(id) == 13:
                            muons += 1
                    except ValueError:
                        pass

            total2e2mu += eventcounter2e2mu
            total4mu += eventcounter4mu
            total4e += eventcounter4e

            print "    2e2mu: %i" % (eventcounter2e2mu,)
            print "      4mu: %i" % (eventcounter4mu,)
            print "       4e: %i" % (eventcounter4e,)

    print "Total:"
    print "    2e2mu: %i" % (total2e2mu,)
    print "      4mu: %i" % (total4mu,)
    print "       4e: %i" % (total4e,)

if __name__ == "__main__":
    import sys
    printleptonfractions(*sys.argv[1:])
