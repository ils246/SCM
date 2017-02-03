from random import randint,choice

def talk(agent,memories,G=None):
    N=len(memories)
    partner = randint(0, N-1)
    while partner == agent:
        if G is None:
            partner = randint(0, N-1)
        else:
            neighs = G.neighbors(agent) #Change this line to upgrade to igraph
            if len(neighs)!=0:
                partner = choice(neighs)
            else:
                return memories
    partner = memories[partner]
    if len(partner) >  0:
        borrowedIdea = choice(list(partner))
        memories[agent].add(borrowedIdea)
    return memories

def think(agent,memories,idea_tick):
    newIdea = idea_tick
    idea_tick+=1
    memories[agent].add(newIdea)
    return memories,idea_tick

def die(agent,memories):
    memories[agent] = set()
    return memories

def countby(f, seq):
    result = {}
    for value in seq:
        key = f(value)
        if key in result:
            result[key] += 1
        else:
            result[key] = 1
    return result
