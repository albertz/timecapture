
def vec_op(vec1, vec2, op):
    return list(map(op, vec1, vec2))

DateVecNorm = (None, 12, 31, 24, 60, 60)
def SumOp(a,b): return a+b
def SubOp(a,b): return a-b

# all of them in reverse order

def vec_stdform(vec, norm):
    def n(x, m):
        if m is None:
            return x, 0
        return x % m, x // m
    while True:
        res = list(map(n, vec, norm))
        vec, rest = zip(*res)
        if not any(rest):
            break
        rest = rest[1:] + (0,)
        vec = vec_op(vec, rest, SumOp)
    return vec

def vec_abs(vec, norm):
    x = 0
    m = 1
    for i in reversed(range(len(vec))):
        x += vec[i] * m
        if norm[i] is None:
            break
        m *= norm[i]
    return x

def vectorize(num, norm):
    vec = ()
    i = len(norm) - 1
    while num != 0:
        m = norm[i]
        if m is not None:
            x = num % m
            num //= m
        else:
            x = num
            num = 0
        vec = (x,) + vec
        i -= 1
        if i < 0:
            break
    return vec
    
def dateAbsDiff(vec1, vec2):
    return vec_abs(vec_op(vec1, vec2, SubOp), DateVecNorm)

def dateVectorize(secs):
    return vectorize(secs, DateVecNorm)

def dateStr(vec):
    if len(vec) == 0:
        return "0 sec"
    if len(vec) == 1:
        return "%d sec" % vec
    if len(vec) == 2:
        return "%d:%02d min" % vec
    if len(vec) >= 3:
        return "%d:%02d:%02d" % vec[-3:]
    return str(vec)
