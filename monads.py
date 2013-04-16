import operator


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


class Either(Monad):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    @classmethod
    def unit(cls, x):
        return cls(None, x)

    @classmethod
    def bind(cls, m, f):
        if m.left:
            return m.left
        else:
            return cls.unit(f(m.right))

    def __repr__(self):
        if self.left:
            inner = "Left(%s)" % self.left
        else:
            inner = "Right(%s)" % self.right
        return "Either:%s" % inner


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
            return cls(f(m.head), cls.bind(m.tail, f))  # should be concat+map?

    def __repr__(self):
        return "List(%s, %s)" % (self.head, repr(self.tail))


class Writer(Monad):

    def __init__(self, x, log=None, combine=None):
        self.x = x
        self.log = log
        if not combine:
            combine = lambda xs, x: xs + [x]
        self.combine = combine

    @classmethod
    def unit(cls, x):
        return cls(x)

    @classmethod
    def bind(cls, m, f):
        nx, nlog = f(m.x)
        return cls(nx, m.combine(m.log, nlog))

    def __repr__(self):
        return "Writer(%s, %s)" % (self.x, self.log)

    def run_writer(self):
        return self.x, self.log

    def exec_writer(self):
        return self.x


if __name__ == "__main__":
    square = lambda x: x * x

    squareWithLog = lambda x: (square(x), "squared(%s)" % x)

    m_id = Identity.unit(2)
    print "m_id", m_id
    print m_id.sbind(square)

    m_maybe = Maybe.unit(3)
    print "m_maybe", m_maybe
    print m_maybe.sbind(square)

    m_maybe_not = Maybe.unit(None)
    print "m_maybe_not", m_maybe_not
    print m_maybe_not.sbind(square)

    m_either_right = Either.unit(4)
    print "m_either_right", m_either_right
    print m_either_right.sbind(square)

    m_either_left = Either("Fake Error", None)
    print "m_either_left", m_either_left
    print m_either_left.sbind(square)

    m_list = List(2, List(3, List(4)))
    print "m_list", m_list
    print m_list.sbind(square)

    m_writer = Writer(5, log=[])
#    m_writer2 = m_writer.sbind(square)
    m_writer3 = m_writer.sbind(squareWithLog)
    print "m_writer", m_writer
#    print "m_writer2", m_writer2
    print "m_writer3", m_writer3
    print "m_writer3.run_writer", m_writer3.run_writer()
    print "m_writer3.exec_writer", m_writer3.exec_writer()
    m_writer4 = m_writer3.sbind(squareWithLog)
    print "m_writer4.run_writer", m_writer4.run_writer()

