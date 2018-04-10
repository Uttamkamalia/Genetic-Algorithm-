import numpy as np


class NeuralNet():


    def __init__(self):
        np.random.seed(1)

        self.w1_r = 9
        self.w1_c = 7
        self.w2_r = 7
        self.w2_c = 4
        self.w1 = 2*np.random.random((self.w1_r,self.w1_c))-1
        self.w2 = 2*np.random.random((self.w2_r,self.w2_c))-1

    def get_dimen(self):
        return [self.w1_r,self.w1_c,self.w2_r,self.w2_c]

    def set_weights(self,weight1,weight2):
        self.w1 = weight1
        self.w2 = weight2


    def get_weights(self):
        return [self.w1,self.w2]

    def sigmoid(self, x, derive=False):
        if (derive == True):
            return x * (1 - x)
        else:
            return 1 / (1 + np.exp(-x))

    def train(self,inputs,outputs,iterations):

        for iter in range(0,iterations):
            a1 = inputs
            a2 = self.sigmoid(np.dot(a1,self.w1))
            a3 = self.sigmoid(np.dot(a2,self.w2))

            err3 = outputs - a3
            delta3 = err3 * self.sigmoid(a3,True)

            err2 = np.dot(delta3,self.w2.T)
            delta2 = err2 * self.sigmoid(a2,True)

            adj2 = np.dot(a2.T,delta3)
            adj1 = np.dot(a1.T,delta2)

            self.w1 += adj1
            self.w2 += adj2
        '''
            if iter%200 == True:
               print("\nWeight 1 at iter:::", iter)
               print(self.w1)
               print("Weight 2 at iter:::", iter)
               print(self.w2)
        '''

    def mapp(self,lis):
        sumo = sum(lis)
        ans = []
        for i in lis:
            ans.append(i / sumo)

        return ans



    def predict(self,inputs,weight1 ,weight2 ):
        a1 = inputs
        a2 = self.sigmoid(np.dot(a1, weight1))
        a3 = self.sigmoid(np.dot(a2, weight2))

        ans = a3.tolist()

        ans = self.mapp(ans)


        return ans
