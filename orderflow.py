class Cpo(object):

    def __init__(self, date, monarch=0, sigma=0):
        self.received = date
        self.monarch = monarch
        self.sigma = sigma
        self.filled = None

class Vpo(object):

    def __init__(self, date, monarch=0, sigma=0):
        self.sent = date
        self.monarch = monarch
        self.sigma = sigma
        self.received = date + 4

class Product(object):

    def __init__(self,name,tq,moq,price,cost):
        self.name = name
        self.tq = tq
        self.moq = moq
        self.price = price
        self.cost = cost
        self.qoh = 20
        self.eqoh = 20
        self.back = 0
        self.wait = 0

class Company(object):

    def __init__(self,endofday):
        self.endofday = endofday
        self.ordernewprod()

    def ordernewprod(self):
        monarchorder = 0
        sigmaorder = 0

        if monarch.tq > (monarch.eqoh + monarch.wait):
            monarchorder =  max(monarch.moq,(monarch.tq - monarch.qoh - monarch.wait + abs(monarch.eqoh - monarch.qoh)))

        if sigma.tq > (sigma.eqoh + sigma.wait):
            sigmaorder =  max(sigma.moq,(sigma.tq - sigma.qoh - sigma.wait + abs(sigma.eqoh - sigma.qoh)))

        if (monarchorder>0) or (sigmaorder>0):
            total_order = Vpo(self.endofday,monarchorder,sigmaorder)
            vpos.append(total_order)
            monarch.wait += monarchorder
            sigma.wait += sigmaorder

        self.processfillcpo()

    def processfillcpo(self):
        #for old cpo stored
        for cpo in cpos:
            if (monarch.qoh > cpo.monarch) and (sigma.qoh>cpo.sigma):
                monarch.qoh -= cpo.monarch
                sigma.qoh -= cpo.sigma
                monarch.back -= cpo.monarch
                sigma.back -= cpo.sigma
                cpo.filled = self.endofday

                print('Day-'+str(self.endofday)+' CPO filled: '+str(cpo.filled)+'-Jan, '+'Received:'+str(cpo.received)+'-Jan, monarch:'+str(cpo.monarch)+', Sigma:'+str(cpo.sigma))
                cpos.pop(cpos.index(cpo))

        #for new cpos received
        for order in orders:
            if order['date'] == self.endofday:
                if (monarch.qoh>order['monarch']) and (sigma.qoh>order['sigma']):
                    monarch.qoh -= order['monarch']
                    sigma.qoh -= order['sigma']

                    print('Day-'+str(self.endofday)+' CPO filled: '+str(order['date'])+'-Jan, '+'Received:'+str(order['date'])+'-Jan, monarch:'+str(order['monarch'])+', Sigma:'+str(order['sigma']))
                    orders.pop(orders.index(order))
                else:
                    newcpo = Cpo(order['date'],order['monarch'],order['sigma'])
                    cpos.append(newcpo)
                    monarch.back += order['monarch']
                    sigma.back += order['sigma']
                    orders.pop(orders.index(order))

        self.processvpo()

    def processvpo(self):
        for vpo in vpos:
            if vpo.received == self.endofday:
                monarch.qoh += vpo.monarch
                sigma.qoh += vpo.sigma
                monarch.wait -= vpo.monarch
                sigma.wait -= vpo.sigma

                print('Day-'+str(self.endofday)+' VPO received: '+str(vpo.received)+'-Jan, '+'Started:'+str(vpo.sent)+'-Jan, monarch:'+str(vpo.monarch)+', Sigma:'+str(vpo.sigma))
                vpos.pop(vpos.index(vpo))

        monarch.eqoh = monarch.qoh - monarch.back
        sigma.eqoh = sigma.qoh - sigma.back

        self.printday()

    def printday(self):
        print('{:>5}  {:>5}  {:>5}  {:>5}  {:>5}'.format(str(self.endofday),str(monarch.eqoh),str(monarch.qoh),str(sigma.eqoh),str(sigma.qoh)))


if __name__ == "__main__":

    from datetime import date

    cpos=[]
    vpos =[]

    n_of_days = (date(2018, 1, 31) - date(2017, 12, 31)).days + 1
    monarch = Product('monarch',20,14,320,200)
    sigma = Product('Sigma',15,10,400,300)

    orders=[
    {'date':1,'monarch':0,'sigma':4},
    {'date':2,'monarch':0,'sigma':13},
    {'date':5,'monarch':0,'sigma':17},
    {'date':7,'monarch':0,'sigma':2},
    {'date':8,'monarch':0,'sigma':5},
    {'date':13,'monarch':22,'sigma':2},
    {'date':15,'monarch':0,'sigma':17},
    {'date':22,'monarch':10,'sigma':5},
    {'date':30,'monarch':0,'sigma':22}]

    print('{:>6}  {:>5}  {:>5}  {:>5}  {:>5}'.format('DATE','MEQOH','MQOH','SEQOH','SQOH'))
    print('-' * 40)
    for date in range(n_of_days):
        hola = Company(date)

        







