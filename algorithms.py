import sys, math, util, hmm

"""
The forward algorith

f_k is a counter where the key are k
a list of f_k represents the passage of time
where the index is t
"""
def forward(model, emissions):
    f = util.Counter()
    for state in model.getStates():
        f[state] = model.p(state)*model.e(state, emissions[0])  
    for b in emissions[1:]:
        f_next = util.Counter()
        for state_l in model.getStates():
            f_next[state_l] = model.e(state_l, b) * sum([model.a(state_k, state_l)*f[state_k] for state_k in model.getStates()])
        f = f_next.copy()
    return f.totalCount()
"""
For the baum-welch algorithm we need f_k(t)
for every state k and for every t in len(emission)
instead of recalculating the same previous values
again we're just gonna store them sequentially
in a list of dictionaries
"""
def getForwardList(model, emissions):
    f = util.Counter()
    for state in model.getStates():
        f[state] = model.p(state)*model.e(state, emissions[0])
    forwardList = [f]  
    for b in emissions[1:]:
        f_next = util.Counter()
        for state_l in model.getStates():
            f_next[state_l] = model.e(state_l, b) * sum([model.a(state_k, state_l)*f[state_k] for state_k in model.getStates()])
        f = f_next.copy()
        forwardList.append(f)
    return forwardList
    
"""
The backward algorithm
"""      
def backward(model, emissions):
    b = util.Counter()
    #minor initialization nuance
    for state in model.getStates() : b[state] = 1
    emissions.reverse()
    for q in emissions[:len(emissions)-1]:
        b_prev = util.Counter()
        for state_k in model.getStates():
            b_prev[state_k] = sum([model.a(state_k, state_l)*model.e(state_l, q)*b[state_l] for state_l in model.getStates()])
        b = b_prev.copy()
    for state in model.getStates():
        b[state] = model.p(state)*model.e(state, emissions[len(emissions)-1])*b[state]
    return b.totalCount()
    
"""
Analogous to getForwardList

Note: we have to return the reversed list because
we iterate backwards and in order for the list index, i 
to match t we must reverse the list
"""   
def getBackwardList(model, emissions):
    b = util.Counter()
    #minor initialization nuance
    for state in model.getStates() : b[state] = 1
    emissions.reverse()
    backwardList = []
    for q in emissions[:len(emissions)-1]:
        b_prev = util.Counter()
        for state_k in model.getStates():
            b_prev[state_k] = sum([model.a(state_k, state_l)*model.e(state_l, q)*b[state_l] for state_l in model.getStates()])
        b = b_prev.copy()
        backwardList.append(b)
    b_last = util.Counter()
    for state in model.getStates():
        b_last[state] = model.p(state)*model.e(state, emissions[len(emissions)-1])*b[state]
    backwardList.append(b_last)
    backwardList.reverse()
    return backwardList


"""
The Baum-Welch Algorithm

"""
def baum_welch(model, sequences, threshold):
    #for now threshold is just an iteration count
    #make this log-likelihood threshold thing
    while threshold > 0:
        #E-Step
        expectedTransitions = util.Counter()
        for k,l in [(k,l) for k in model.getStates() for l in model.getStates()]:
            total = 0.0
            for sequence in sequences:
                forwardList = getForwardList(model, sequence)
                backwardList = getBackwardList(model, sequence)
                for t in range(len(sequence)-1):
                    total += (forwardList[t][k]*model.a(k,l)*model.e(l,sequence[t+1])*backwardList[t+1][l])/forward(model, sequence[:t+1])
            expectedTransitions[(k,l)] = total
        expectedEmissions = util.Counter()
        for k,b in [(k,b) for b in model.getEmissions() for k in model.getStates()]:
            total = 0.0
            for sequence in sequences:
                forwardList = getForwardList(model, sequence)
                backwardList = getBackwardList(model, sequence)
                for t in range(len(sequence)-1):
                    if sequence[t] == b:
                        total += forwardList[t][k]*backwardList[t][k]/forward(model, sequence[:t+1])
            expectedEmissions[(k,b)] = total
        print expectedEmissions
        #M-Step
        new_a = {}
        for k,l in [(k,l) for k in model.getStates() for l in model.getStates()]:
            new_a[(k,l)] = expectedTransitions[(k,l)]/sum([expectedTransitions[(k,l_2)] for l_2 in model.getStates()])
        new_e = {}
        for k,b in [(k,b) for b in model.getEmissions() for k in model.getStates()]:
            new_e[(k,b)] = expectedEmissions[(k,b)]/sum([expectedEmissions[(k,b_2)] for b_2 in model.getEmissions()])
        model = hmm.HMM(model.getStates(), model.getEmissions(), new_a, new_e, model.getMarginal())
        print new_a
        print new_e
        print "\n\n"
        threshold -= 1
                
                
            
            
            
            
            
            
            
            
            
            
            
  
