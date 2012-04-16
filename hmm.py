import sys, math

class HMM:
    #I'm not sure if the error checking is a good idea since we're gonna be changing parameters
    #once we do EM
    
    def a(self,k,l):
        if self.isAHiddenState(k) and self.isAHiddenState(l):
            return self.transitionProbabilities[(k,l)]
        else:
            print "ERROR: k=%s or l=%s not a hidden state" % (k,l)
            return
        
    def e(self,k,b):
        if not self.isAnEmission(b):
            print "ERROR: b=%s is not an emission" % b
            return
        if not self.isAHiddenState(k):
            print "ERROR k=%s is not a hidden state" % k
            return
        return self.emissionProbabilities[(k,b)]
        
    def p(self, k):
        if not self.isAHiddenState(k):
            print "ERROR k=%s is not a hidden state" % k
            return
        return self.marginal[k]
        
    def getMarginal(self):
        return self.marginal
        
    def getStates(self):
        return self.stateSpace
    
    def getEmissions(self):
        return self.emissions
        
    #############################################
    #             Helper methods:               #          
    # You shouldn't need to call these directly #
    #############################################
    """
    s is a list of hidden states
    q is a list of emission states
    a is a dictionary of transition probailities k to l with (k,l) as keys
    e is a dictionary of emission probabilities b from k with (k, b) as the keys
    marginal is the marginal probability that Q_1 = k, this is a dictionary with 
        k as the key
    """
    def __init__(self, s, q, a, e, marginal):
        self.stateSpace = s
        self.emissions = q
        self.transitionProbabilities = a
        self.emissionProbabilities = e
        self.marginal = marginal
    
    def isAHiddenState(self, s):
        return s in self.stateSpace
        
    def isAnEmission(self, q):
        return q in self.emissions
        
    def __str__(self):
        s = "Hidden States:\n" + str(self.stateSpace) + "\n"
        s += "Emission States:\n" + str(self.emissions) + "\n"
        s += "Tranistion Probabilities:\n" + str(self.transitionProbabilities) + "\n"
        s += "Emission Probabilities:\n" + str(self.emissionProbabilities) + "\n"
        s += "Marginals:\n" + str(self.marginal)
        return s
    
