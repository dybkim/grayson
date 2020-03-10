import numpy as np

class Kalman_Filter(object):
    def __init__(self):
        self.x = 0.0
        self.states = {}
        
        # State Uncertainty Covariance  Matrix
        self.p_matrix = np.array([[0.1, 0.0, 0.0, 0.0, 0.0, 0.0],
                                    [0.0, 0.005, 0.0, 0.0, 0.0, 0.0],
                                    [0.0, 0.0, 0.005, 0.0, 0.0, 0.0],
                                    [0.0, 0.0, 0.0, 0.0001, 0.0, 0.0],
                                    [0.0, 0.0, 0.0, 0.0, 0.00001, 0.0],
                                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.01]])
    
        # Measurement Function
        self.h_matrix = np.array([[1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                 [0.0, 1.0, 0.0, 0.0, 0.0, 0.0]])
        
        self.i_matrix = np.identity(6)
        
        # Measurement White Noise Matrix
        self.r_matrix = np.array([[0.03, 0.0],
                                 [0.0, 0.03]])
        
    def observation_step(self, measured_value):
        # Utilize measurement step in Kalman Filter
        x = measured_value.data[0]
        y = measured_value.data[1]
        deltaT = measured_value.deltaT
        z = np.array([x, y])
        
        # State Transition Function
        f_matrix = np.array([[1.0, 0.0, 1.0 * deltaT, 0.0, 0.5 * (deltaT * deltaT), 0.0],
                             [0.0, 1.0, 0.0, 1.0 * deltaT, 0.0, 0.5 * (deltaT * deltaT)],
                             [0.0, 0.0, 1.0, 0.0, 1.0 * deltaT, 0.0],
                             [0.0, 0.0, 0.0, 1.0, 0.0, 1.0 * deltaT],
                             [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                             [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]])
        
        # y=z-H*x - Innovation: the difference between measured value and predicted value
        # z: 2x1
        # H: 2x6
        # x: 6x1
        # y: 2x1 
        y_matrix = z - self.h_matrix @ self.state

        # S=H*P*Ht+R - Innovation Error Covariance Matrix
        # H: 2x6
        # P: 6x6
        # Ht: 6x2
        # R: 2x2
        s_matrix = self.h_matrix @ self.p_matrix @ self.h_matrix.transpose() + self.r_matrix

        # K=P*Ht*Sinv - Kalman Gain: A measure of how much weight (or how much we believe in) the measured value 
        # P: 6x6
        # Ht: 6x2
        # Sinv: 2x2
        # K: 6x2
        k_matrix = self.p_matrix @ self.h_matrix.transpose() @ np.linalg.inv(s_matrix)

        # x=x+K*y
        # x: 6x1
        # K: 6x2
        # y: 2x1
        self.state = self.state + k_matrix @ y_matrix

        # P = (I-K*H)*P
        # I: 6x6
        # K: 6x2
        # H: 2x6
        # P: 6x6

        self.p_matrix = (self.i_matrix - (k_matrix @ self.h_matrix)) @ self.p_matrix
    
    def prediction_step(self):
        #Use Kalman Prediction step

        # x=F*x+u
        # F: 6x6
        # x: 6x1
        self.state = self.f_matrix @ self.state

        # P=F*P*Ft
        # F: 6x6
        # P: 6x6
        # Ft: 6x6
        self.p_matrix = self.f_matrix @ self.p_matrix @ self.f_matrix.transpose()
