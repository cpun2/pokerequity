import collections
import random

def listtonum(cards):
    return cards[0]*10000 + cards[1]*1000 + cards[2]*100 + cards[3]*10 + cards[4]

def winner(handa,handb,bha,bhb):
    if bha[0] < bhb[0]:
        print("Player with hand")
        print(handa)
        print("wins with")
        print()
    elif bhb[0] < bha[0]:
        print("Player with hand")
        print(handb)
        print("wins")
    else:
        bestcardsa = bha[1]
        bestcardsb = bhb[1]
        for i in range(5):
            if bestcardsa[i] > bestcardsb[i]:
                print("Player with hand")
                print(handa)
                print("wins")
                return
            if bestcardsa[i] < bestcardsb[i]:
                print("Player with hand")
                print(handb)
                print("wins")
                return
        print("Its a tie")

def straight(cards):
    cards = list(map(lambda x: x[0], cards))
    currstraight = [cards[len(cards)-1]]
    i = len(cards)-2
    while i >= 0:
        if cards[i+1] == cards[i] + 1:
            currstraight.append(cards[i])
            if len(currstraight) == 5:
                return currstraight
            if len(currstraight) == 4 and currstraight[len(currstraight)-1] == 2:
                if cards[len(cards)-1] == 14:
                    currstraight.append(cards[len(cards)-1])
                    return currstraight
        elif cards[i+1] == cards[i]:
            i = i - 1
            continue
        else:
            currstraight = [cards[i]]
        i = i - 1
    return []

def besthand(seven):
    seven.sort()
    suit0 = list(filter(lambda x: x[1] == 0, seven))
    suit1 = list(filter(lambda x: x[1] == 1, seven))
    suit2 = list(filter(lambda x: x[1] == 2, seven))
    suit3 = list(filter(lambda x: x[1] == 3, seven))
    suits = [suit0,suit1,suit2,suit3]
    flushfilter = list(filter(lambda x: len(x) >= 5, suits))
    if len(flushfilter) > 0:
        flush = flushfilter[0]
        straightflush = straight(flush)
        if len(straightflush) > 0:
            return (0,straightflush)
    nosuit = list(map(lambda x: x[0],seven))
    nosuit.reverse()
    counter = collections.Counter(nosuit)
    removedups = list(dict.fromkeys(nosuit))
    sets = []
    pairs = []
    for i in removedups:
        if counter[i] == 4:
            removedups.remove(i)
            return (1,[i,i,i,i,removedups[0]])
        if counter[i] == 3:
            sets.append(i)
            pairs.append(i)
        elif counter[i] == 2:
            pairs.append(i)
    if len(sets) > 0:
        pairs.remove(sets[0])
        if len(pairs) > 0:
            return (2,[sets[0],sets[0],sets[0],pairs[0],pairs[0]])
    if len(flushfilter) > 0:
        return (3,list(map(lambda x: x[0],flushfilter[0])))
    checkstraight = straight(seven)
    if len(checkstraight) > 0:
        return (4,checkstraight)
    if len(sets) > 0:
        removedups.remove(sets[0])
        return (5,[sets[0],sets[0],sets[0],removedups[0],removedups[1]])
    if len(pairs) > 0:
        removedups.remove(pairs[0])
        if len(pairs) > 1:
            removedups.remove(pairs[1])
            return (6,[pairs[0],pairs[0],pairs[1],pairs[1],removedups[0]])
        return(7,[pairs[0],pairs[0],removedups[0],removedups[1],removedups[2]])
        #index out of bounds here idk why
    return (8,removedups[:5])

def compute(hands,numplayers):

    cards = [(i,j) for i in range(2,15) for j in range(4) if ((i,j) not in hands)]
    k = 100000
    pairsofhands = []
    for i in range(numplayers):
        currhand = (hands[i*2],hands[i*2+1])
        pairsofhands.append(currhand)
    wins = [[0,0] for i in range(len(pairsofhands))]
    for i in range(k):
        random.shuffle(cards)
        river = cards[:5]
        besthands = []
        for x in pairsofhands:
            currseven = list(x) + river
            besthands.append(besthand(currseven))

        handtier = list(map(lambda x: x[0],besthands))
        highesthand = min(handtier)
        winninghands = list(filter(lambda x: x[1][0] == highesthand, enumerate(besthands)))
        if len(winninghands) == 1:
            wins[winninghands[0][0]][0] += 1
            continue
        comparingsametier = list(map(lambda x: (x[0],listtonum(x[1][1])),winninghands))
        #print(comparingsametier)
        handnumber = list(map(lambda x: x[1], comparingsametier))
        winningnumber = max(handnumber)
        winning = list(filter(lambda x: x[1] == winningnumber, comparingsametier))
        if len(winning) == 1:
            wins[winning[0][0]][0] += 1
        else:
            for x in winning:
                wins[x[0]][1] += 1




        # if bha[0] < bhb[0]:
        #     awin = awin + 1
        # elif bhb[0] < bha[0]:
        #     bwin = bwin + 1
        # else:
        #     bestcardsa = bha[1]
        #     bestcardsb = bhb[1]
        #     willtie = True
        #     for j in range(5):
        #         if bestcardsa[j] > bestcardsb[j]:
        #             awin = awin + 1
        #             willtie = False
        #             break
        #         if bestcardsa[j] < bestcardsb[j]:
        #             bwin = bwin + 1
        #             willtie = False
        #             break
        #     if willtie:
        #         tie = tie + 1

    suit = {}
    suit[0] = "d"
    suit[1] = "c"
    suit[2] = "h"
    suit[3] = "s"
    val = {}
    val[14] = "A"
    val[13] = "K"
    val[12] = "Q"
    val[11] = "J"
    for i in range(len(pairsofhands)):
        currcard1val = pairsofhands[i][0][0]
        currcard1suit = pairsofhands[i][0][1]
        currcard2val = pairsofhands[i][1][0]
        currcard2suit = pairsofhands[i][1][1]
        currcardstring = "Player " + str(i+1) + " with hand: "
        if currcard1val in val:
            currcardstring += val[currcard1val]
        else:
            currcardstring += str(currcard1val)
        currcardstring = currcardstring + suit[currcard1suit] + " "
        if currcard2val in val:
            currcardstring += val[currcard2val]
        else:
            currcardstring += str(currcard2val)
        currcardstring = currcardstring + suit[currcard2suit]
        print(currcardstring)
        probstr = "Wins " + str(wins[i][0]*100/k) + "% of times and ties " + str(wins[i][1]*100/k) + "% of the time."
        print(probstr)

    #print(wins)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dict = {}
    dict["A"] = 14
    dict["K"] = 13
    dict["Q"] = 12
    dict["J"] = 11
    suit = {}
    suit["d"] = 0
    suit["c"] = 1
    suit["h"] = 2
    suit["s"] = 3
    print("How many players?")
    handcount = input()
    hands = []
    for i in range(int(handcount)):
        question1 = "What is player " + str(i+1) + "'s first card?"
        print(question1)
        card1val = input()
        print("suit?")
        card1suit = input()
        question2 = "What is player " + str(i + 1) + "'s second card?"
        print(question2)
        card2val = input()
        print("suit?")
        card2suit = input()

        if card1val in dict:
            card1 = (dict[card1val],suit[card1suit])
        else:
            card1 = (int(card1val),suit[card1suit])
        if card2val in dict:
            card2 = (dict[card2val],suit[card2suit])
        else:
            card2 = (int(card2val),suit[card2suit])
        hands.append(card1)
        hands.append(card2)
    compute(hands,int(handcount))

    #compute([(14,2),(6,1),(9,1),(8,0),(10,0),(10,1)],3)