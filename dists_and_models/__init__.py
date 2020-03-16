from typing import List
import numpy as np

class Gamma:
    def __init__(self, *, a, b):
        self.a = a
        self.b = b
        
    def get():
        """ ガンマ分布をscipyのfrozen RV objectの形で返す。
        Notes:
            scipyのgamma distは、教科書の定義とちょっと異なる。教科書で言うハイパーパラメーターbは、
            scaleという名前で指定する。
            https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gamma.html
        """
        return [stats.gamma(a=elem, scale=b) for elem in self.a]


class Poisson:
    def __init__(self, *, lambda_: List[float]):
        self.lambda_ = lambda_

    def get():
        """ ポアソン分布をscipyのfrozen RV objectの形で返す。"""
        return [stats.poisson(mu=elem) for elem in self.lambda_]


class BayesPoiMixModel:
    def __init__(self, *, num_dim: int, num_cluster: int, alpha, gamma):
        """ ポアソン混合モデルの事前・事後分布を表現するクラスを構築する。
        Args:
            D: 観測データの次元
            K: クラスター数
            alpha : カテゴリ分布のパラメーター $\pi$ の共役事前分布であるディリクレ分布のハイパーパラメーター (p.119)
            gamma : ポアソン分布のパラメーター $\lambda$ の共役事前分布であるガンマ分布のハイパーパラメーター (p.129)
                * 非リストを指定した場合、全クラスターに同じ値を指定する。
                * リストを指定した場合、各クラスターにおのおの指定された値を指定する。
        Notes:
            len(gamma) != num_clusterの場合は例外を投げる。
        """
        self.num_dim = num_dim
        self.num_cluster = num_cluster
        self.alpha = np.ones(num_cluster) * alpha
        if isinstance(gamma, list):
            if len(gamma) != num_cluster:
                raise "in BayesPoiMixModel.__init__() : len(gamma) != num_cluster"
            self.gamma = gamma
        else: 
            self.gamma = [gamma]*num_cluster


class PoiMixModel:
    def __init__(self, *, num_dim: int, num_cluster: int, phi, poisson: Poisson):
        """ 真のポアソン混合モデルを構築する。
        Args:
            D: 観測データの次元
            K: クラスター数
            alpha : 
            poiDists: 
        """
        self.num_dim = num_dim
        self.num_cluster = num_cluster
        self.phi = phi
        if isinstance(poisson, list):
            if len(poisson) != num_cluster:
                raise "in PoiMixModel.__init__() : len(poisson) != num_cluster"
            self.poisson = poisson
        else: 
            self.poisson = [poisson]*num_cluster
