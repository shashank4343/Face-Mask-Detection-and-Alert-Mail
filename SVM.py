

from sklearn import svm
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.metrics import precision_recall_curve
from sklearn.model_selection import cross_validate
import os as os
from sklearn.model_selection import cross_val_score
from sklearn import metrics
from sklearn import linear_model


###########################
# LOADING TRAINING DATA
###########################
os.chdir('C:/Users/Mrida/Documents/Python/who-is-more-influential-master/Original Dataset')
trainfile = open('train.csv')
for line in trainfile:
    header = line.rstrip().split(',')
    break

y_train = []
X_train_A = []
X_train_B = []

for line in trainfile:
    splitted = line.rstrip().split(',')
    label = int(splitted[0])
    A_features = [float(item) for item in splitted[1:12]]
    B_features = [float(item) for item in splitted[12:]]
    y_train.append(label)
    X_train_A.append(A_features)
    X_train_B.append(B_features)
trainfile.close()

y_train = np.array(y_train)
X_train_A = np.array(X_train_A)
X_train_B = np.array(X_train_B)

def transform_features(x):
    return np.log(1+x)
    #x = (x - np.mean(x,axis = 0))/np.std(x,axis = 0) 
    #return x

X_train = transform_features(X_train_A) - transform_features(X_train_B)
model=svm.SVC(probability=True);
model2=linear_model.LogisticRegression(fit_intercept=False).fit(X_train, y_train)
C = 1.0  # SVM regularization parameter
#model = svm.SVC(kernel='linear', C=C, probability=True).fit(X_train, y_train) #SVM with Linear Kernel
model = svm.SVC(kernel='rbf', C=C, probability=True).fit(X_train, y_train) #rbf_svm
#model = svm.SVC(kernel='poly', degree=3, C=C, probability=True).fit(X_train, y_train) #Polynomial SVM
#model = svm.LinearSVC(C=C).fit(X_train, y_train) #Linear SVM

#20 Fold Cross Validation Score
#print("20 Fold CV Score: ", cross_val_score(model, X_train, y_train, cv=20, scoring='roc_auc'))


# Logistic regression # 


p_train1 = model2.predict_proba(X_train)
#accuracy = metrics.accuracy_score(y_train, p_train1)
p_train1 = p_train1[:,1:2]
precision, recall, thresholds=precision_recall_curve(y_train,p_train1[:,0])
#accuracy = metrics.accuracy_score(y_train, p_train1[:,0])
print("******************Logistic Regression Accuracy******************")
#print(accuracy)
print('AuC score on training data:',roc_auc_score(y_train,p_train1[:,0]))



# compute AuC score on the training data (BTW this is kind of useless due to overfitting, but hey, this is only an example solution)
p_train = model.predict_proba(X_train)
p_train = p_train[:,1:2]
precision, recall, thresholds=precision_recall_curve(y_train,p_train[:,0])
#accuracy = metrics.accuracy_score(y_train, p_train[:,0])
print("******************Support vector Machine Accuracy******************")
#print(accuracy)
print('AuC score on training data:',roc_auc_score(y_train,p_train[:,0]))

###########################
# READING TEST DATA
###########################

testfile = open('C:\\Users\\Mrida\\Documents\\Python\\who-is-more-influential-master\\Original Dataset\\test.csv')
#ignore the test header
for line in testfile:
    break

X_test_A = []
X_test_B = []
for line in testfile:
    splitted = line.rstrip().split(',')
    A_features = [float(item) for item in splitted[0:11]]
    B_features = [float(item) for item in splitted[11:]]
    X_test_A.append(A_features)
    X_test_B.append(B_features)
testfile.close()

X_test_A = np.array(X_test_A)
X_test_B = np.array(X_test_B)

# transform features in the same way as for training to ensure consistency
X_test = transform_features(X_test_A) - transform_features(X_test_B)

# compute probabilistic predictions
p_test = model.predict_proba(X_test)
#only need the probability of the 1 class
p_test = p_test[:,1:2]

###########################
# WRITING SUBMISSION FILE
###########################
predfile = open('predictions.csv','w+')
predfile.write('Id,Choice\n')
i=1;
for line in p_test:
    x=str(i)+','+str(line[0])
    predfile.write(x)
    predfile.write('\n')
    i=i+1

predfile.close()