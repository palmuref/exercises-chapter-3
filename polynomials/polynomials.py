from numbers import Number, Integral


class Polynomial:

    def __init__(self, coefs):
        # remove trailing zeros from the coefficent list
        while coefs[-1] == 0 and len(coefs) > 1:
            coefs = coefs[:-1]
        self.coefficients = coefs

    def degree(self):
        return len(self.coefficients) - 1

    def __str__(self):
        # could be improved in that x^1 is replaced just by x.
        coefs = self.coefficients

        # initialize string
        string = ""

        # start with the constant term, if nonzero
        if coefs[0] != 0:
            string += "{}".format(coefs[0])

        for (k, a) in enumerate(coefs[1:]):
            # zero coefficients do not appear in the string
            if a == 0:
                continue
            # negative coefficients get a - instead of a +
            if a < 0:
                string += " - {}x^{}".format(abs(a), k+1)
            # if the coefficient is 1, only x^k appears
            elif a == 1:
                string += " + x^{}".format(k+1)
             # if the coefficient is -1, only x^k appears
            elif a == -1:
                string += " - x^{}".format(k+1)
            # case of positive coefficient
            else:
                string += " + {}x^{}".format(a, k+1)

        return string

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.coefficients) + ")"

    def __eq__(self, other):

        return isinstance(other, Polynomial) and\
             self.coefficients == other.coefficients

    def __add__(self, other):

        if isinstance(other, Polynomial):
            common = min(self.degree(), other.degree()) + 1
            coefs = tuple(a + b for a, b in zip(self.coefficients,
                                                other.coefficients))
            coefs += self.coefficients[common:] + other.coefficients[common:]

            return Polynomial(coefs)

        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] + other,)
                              + self.coefficients[1:])

        else:
            return NotImplemented

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        neg_coefficients = tuple([-c for c in self.coefficients])
        return Polynomial(neg_coefficients)

    def __sub__(self, other):
        # Apparently f - g is logically different than f + (-g),
        # so the parentesis below is needed (get a RecursionError instead).
        # Also, with this method it is not needed to define __rsub__
        return self + (-other)

    def __mul__(self, other):
        """Product of two polynomials.
        For the coefficients we use the "Cauchy product".
        """

        # case of other == scalar
        if isinstance(other, Number):
            coef_prod = tuple(other * a for a in self.coefficients)

        # case of other == Polynomial
        elif isinstance(other, Polynomial):

            # get the coefficients of the polynomials
            coef_self = self.coefficients
            coef_other = other.coefficients

            # get the length of the coefficient tuples, i.e. the degree + 1
            len_self = len(coef_self)
            len_other = len(coef_other)

            # add complementary zero-coefficients
            # to each coefficient tuple
            coef_self += len_self * (0,)
            coef_other += len_other * (0,)

            # compute the product coefficient tuple
            coef_prod = ()
            for i in range(1, len_self + len_other):
                coef_self_ith = coef_self[:i]
                coef_other_ith = coef_other[:i]
                coef_prod_ith = sum(a*b for a, b in zip(coef_self_ith, coef_other_ith[::-1]))
                coef_prod += (coef_prod_ith, )

        # case of other == none of the above
        else:
            return NotImplemented

        return Polynomial(coef_prod)

    def __rmul__(self, other):
        # other * self raises a RecursionError
        return self.__mul__(other)

    def __pow__(self, other):

        if isinstance(other, Integral) and other >= 0:

            if other == 0:
                return Polynomial((1,))

            i = other
            p = Polynomial((1,))
            while i > 0:
                p *= self
                i -= 1
            return p
            # for some reason the following does not work
            #return self * self.__pow__(other-1)

        else:
            return NotImplemented


    def __call__(self, other):

        if isinstance(other, Number):
            return sum(a * other**k for k, a in enumerate(self.coefficients))

        else:
            return NotImplemented

    def dx(self):
        """Returns the derivative of the polynomial"""
        # Note: this method does not apply to numerical constants, so e.g. 7.dx() does not work

        # case of constant polynomial
        if self.degree() == 0:
            return Polynomial((0,))

        # case of self.degree() > 0 i.e. self not constant
        coef_der = tuple((k+1) * a for (k, a) in enumerate(self.coefficients[1:]))

        return Polynomial(coef_der)




