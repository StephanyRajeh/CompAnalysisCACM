def numberOfRecoveredNodes(R):
    timeTillSteadyState = len(R)
    finalIndex = timeTillSteadyState - 1
    if finalIndex==-1:
        return 0
    else:
        return R[finalIndex]