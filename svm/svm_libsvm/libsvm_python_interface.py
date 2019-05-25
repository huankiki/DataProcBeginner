######################################
## Same as sklearn, load data and scale
#Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#Importing the dataset
dataset = pd.read_csv('./Social_Network_Ads.csv')
X = dataset.iloc[:, [2, 3]].values
y = dataset.iloc[:, 4].values

#Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

#Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

######################################
kernel_dict = {
    "Linear": "0",
    "poly": '1',
    "rbf": "2"
}
## train and predict using libsvm
import sys
sys.path.append('/home/liushuhuan/Downloads/libsvm/python')
from svmutil import *
prob = svm_problem(y_train, X_train)

###### Kernel
kernel_type = "rbf"
param = svm_parameter('-t ' + kernel_dict[kernel_type] + ' -c 4 -b 1 -h 0')
m = svm_train(prob, param)
y_pred, y_acc, y_val = svm_predict(y_test, X_test, m, '-b 1')
ACC, MSE, SCC = evaluations(y_test, y_pred)

######################################
## evaluation
#Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
cm = confusion_matrix(y_test, y_pred)
print("\n")
print(cm)
print(classification_report(y_test, y_pred))

#Visualising the Test set results
from matplotlib.colors import ListedColormap
X_set, y_set = X_test, y_test
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))

point_num = np.array([X1.ravel(), X2.ravel()]).shape[1]
## !!!!!! 注意一个bug，最初np.ones((point_num, 1), 这是错误的，变成二维矩阵了，而不是一维数组，所以一直报错
## AttributeError: 'bool' object has no attribute 'mean'
Y12 = np.ones((point_num, ), dtype=np.float64)

## 得到预测值Y_pred
## 为什么要用ravel，参看：https://stackoverflow.com/questions/35811273/scikit-learn-and-data-visusalisation-why-do-i-have-to-use-ravel-when-i-use-pred
Y_pred, y_acc, y_val = svm_predict(Y12, (np.array([X1.ravel(), X2.ravel()]).T), m, '-b 1')
## AttributeError: 'list' object has no attribute 'reshape'
plt.contourf(X1, X2, np.array(Y_pred).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('red', 'green')))

plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('red', 'green'))(i), label = j)
plt.title('SVM (Test set)' + ', kernel: ' + kernel_type)
plt.xlabel('Age')
plt.ylabel('Estimated Salary')
plt.legend()
plt.show()
