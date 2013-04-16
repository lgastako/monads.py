class Monad:

    @classmethod
    def unit(cls, x):
        raise NotImplementedError

    @classmethod
    def bind(cls, m, f):
        raise NotImplementedError

    def sbind(self, f):
        return self.bind(self, f)


class Identity(Monad):

    def __init__(self, x):
        self.x = x

    @classmethod
    def unit(cls, x):
        return cls(x)

    @classmethod
    def bind(cls, m, f):
        return cls.unit(f(m.x))

    def __repr__(self):
        return "Identity(%s)" % self.x


class Maybe(Monad):

    def __init__(self, x):
        self.x = x

    @classmethod
    def unit(cls, x):
        return cls(x)

    @classmethod
    def bind(cls, m, f):
        if m.x:
            return cls.unit(f(m.x))
        return m

    def __repr__(self):
        return "Maybe(%s)" % self.x


class List(Monad):

    def __init__(self, head, tail=None):
        self.head = head
        self.tail = tail

    @classmethod
    def unit(cls, x):
        return cls(x)

    @classmethod
    def bind(cls, m, f):
        if m.tail is None:
            return cls.unit(f(m.head))
        else:
            return cls(f(m.head), cls.bind(m.tail, f))

    def __repr__(self):
        return "List(%s, %s)" % (self.head, repr(self.tail))


if __name__ == "__main__":
    double = lambda x: x * x

    a, b, c = 2, 3, 4

    m_id = Identity.unit(a)
    print "m_id", m_id
    print m_id.sbind(double)

    m_maybe = Maybe.unit(b)
    print "m_maybe", m_maybe
    print m_maybe.sbind(double)

    m_maybe_not = Maybe.unit(None)
    print "m_maybe_not", m_maybe_not
    print m_maybe_not.sbind(double)

    m_list = List(a, List(b, List(c)))
    print "m_list", m_list
    print m_list.sbind(double)

