import visualize

def testSteering():
    print(visualize._visSteering(1.0) + " 1.0")
    print(visualize._visSteering(0.9) + " 0.9")
    print(visualize._visSteering(0.8) + " 0.8")
    print(visualize._visSteering(0.7) + " 0.7")
    print(visualize._visSteering(0.6) + " 0.6")
    print(visualize._visSteering(0.5) + " 0.5")
    print(visualize._visSteering(0.4) + " 0.4")
    print(visualize._visSteering(0.3) + " 0.3")
    print(visualize._visSteering(0.2) + " 0.2")
    print(visualize._visSteering(0.1) + " 0.1")
    print(visualize._visSteering(0.0) + " 0.0")
    print(visualize._visSteering(-0.0) + " -0.0")
    print(visualize._visSteering(-0.1) + " -0.1")
    print(visualize._visSteering(-0.2) + " -0.2")
    print(visualize._visSteering(-0.3) + " -0.3")
    print(visualize._visSteering(-0.4) + " -0.4")
    print(visualize._visSteering(-0.5) + " -0.5")
    print(visualize._visSteering(-0.6) + " -0.6")
    print(visualize._visSteering(-0.7) + " -0.7")
    print(visualize._visSteering(-0.8) + " -0.8")
    print(visualize._visSteering(-0.9) + " -0.9")
    print(visualize._visSteering(-1.0) + " -1.0")


if __name__ == "__main__":
    testSteering()