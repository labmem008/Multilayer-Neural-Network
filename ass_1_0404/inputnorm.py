from parameter import Parameter
import numpy as np
class InputNorm:
    def __init__(self, shape, is_test=False):
        
        self.eps = 1e-8
        self.is_test = is_test
        self.coe = 0.02
        self.overall_var = Parameter(np.zeros(shape))
        self.overall_ave = Parameter(np.zeros(shape))

    def forward(self, x):
        if self.is_test:
            # 进行测试时使用估计的训练集的整体方差和均值进行归一化
            sample_ave = self.overall_ave.data
            sample_std = np.sqrt(self.overall_var.data)
        else:
            # 进行训练时使用样本的均值和方差对训练集整体的均值和方差进行估计（使用加权平均的方法）
            sample_ave = x.mean(axis=0)
            sample_var = x.var(axis=0)
            sample_std = np.sqrt(sample_var + self.eps)
            self.overall_ave.data = (1 - self.coe) * self.overall_ave.data + self.coe * sample_ave
            self.overall_var.data = (1 - self.coe) * self.overall_var.data + self.coe * sample_var
        return (x - sample_ave) / sample_std

    def backward(self,eta):
        return
