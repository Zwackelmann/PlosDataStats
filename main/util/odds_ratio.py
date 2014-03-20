from sklearn.feature_extraction.text import CountVectorizer

tokenizer = CountVectorizer().build_tokenizer()

def oddsRatioForEachFactor(targetItems, otherItems):
    numTargetItems = len(targetItems)
    numOtherItems = len(otherItems)

    factorMapTarget = { }
    factorMapOther = { } 

    factorSet = set()

    for item in targetItems:
        factors = set(item)
        factorSet |= factors
        
        for factor in factors:
            factorMapTarget[factor] = factorMapTarget.get(factor, 0) + 1

    for item in otherItems:
        factors = set(item)
        factorSet |= factors
        
        for factor in factors:
            factorMapOther[factor] = factorMapOther.get(factor, 0) + 1

    def numItemsTargetAndFactor(factor):
        return factorMapTarget.get(factor, 0)
    def numItemsTargetAndNotFactor(factor):
        return numTargetItems - factorMapTarget.get(factor, 0)
    def numItemsNotTargetAndFactor(factor):
        return factorMapOther.get(factor, 0)
    def numItemsNotTargetAndNotFactor(factor):
        return numOtherItems - factorMapOther.get(factor, 0)

    def score(factor):
        if numItemsTargetAndFactor(factor) == 0 or numItemsNotTargetAndNotFactor(factor) == 0:
            return 0.0
        elif numItemsTargetAndNotFactor(factor) == 0 or numItemsNotTargetAndFactor(factor) == 0:
            return float("inf")
        else:
            return (float(numItemsTargetAndFactor(factor)) * numItemsNotTargetAndNotFactor(factor)) / (long(numItemsTargetAndNotFactor(factor)) * numItemsNotTargetAndFactor(factor))

    return map(lambda x: [x, score(x)], factorSet)

