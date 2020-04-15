import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scikitplot as skplt
from sklearn.model_selection import train_test_split as tts
from sklearn.ensemble import RandomForestClassifier,RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier,DecisionTreeRegressor
from sklearn.metrics import confusion_matrix,accuracy_score,r2_score,mean_squared_error,roc_auc_score,roc_curve,auc, f1_score, precision_score, recall_score
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelBinarizer,label_binarize
from sklearn.multiclass import OneVsRestClassifier
import numpy as np
import random
import wx 
import sys 

rainfall=pd.read_csv(r"maharashtra_rainfall.csv")
fer=pd.read_csv(r"proper_dataset.csv")
cropdb=pd.read_csv(r"crop_db.csv")
rainfall.dtypes
fer.dtypes


fer.hist(figsize=(10,8))


fer.plot(kind= 'box' , subplots=True, layout=(3,3), sharex=False, sharey=False, figsize=(10,8))

plt.show()

rainfall=rainfall.drop(['state'],axis=1)

rainfall_X = rainfall.drop(['rain'],axis=1)
rainfall_y = rainfall['rain']

fer_X=fer.drop(['fertility'],axis=1)
fer_y=fer['fertility']

rainfall_X=pd.get_dummies(rainfall_X)

a=random.random()


X_rainfall_train, X_rainfall_test, y_rainfall_train, y_rainfall_test = tts(
    rainfall_X,
    rainfall_y,
    test_size=0.2)

X_fer_train, X_fer_test, y_fer_train, y_fer_test = tts(
    fer_X,
    fer_y,
    test_size=0.2)
  


def multiclass_roc_auc_score(y_test, y_pred, average="macro"):
    lb = LabelBinarizer()
    lb.fit(y_test)
    y_test = lb.transform(y_test)
    y_pred = lb.transform(y_pred)
    return roc_auc_score(y_test, y_pred, average=average)

#Decision Tree Classification
def run_decision_tree_classification(X_train,X_test,y_train,y_test,fertility_columns_test):
    clf_entropy = DecisionTreeClassifier(criterion = "entropy", random_state = 100,max_depth = 3, min_samples_leaf = 5) 
    clf_entropy.fit(X_train, y_train)  
    print("Decision_tree:train set")
    y_pred = clf_entropy.predict(X_train)
    print("Decision_tree:Confusion Matrix:\n ", confusion_matrix(y_train, y_pred))
    auc1 = multiclass_roc_auc_score(y_train,y_pred)
    print('AUC for Decision Tree:',auc1)
    y_score = clf_entropy.predict_proba(X_train)
    n_classes=3
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    y_train1 = label_binarize(y_train, classes=[0, 1, 2])
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_train1[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    colors = list(['blue', 'red', 'green'])
    for i, color in zip(range(n_classes), colors):
        plt.plot(fpr[i], tpr[i], color=color,label='ROC curve of class {0} (area = {1:0.2f})'''.format(i, roc_auc[i]))
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([-0.05, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC-AUC curve')
    plt.legend(loc="lower right")
    plt.show()
    print ("Decision_tree:Accuracy : ", accuracy_score(y_train,y_pred)*100)
    print("Error rate for Decision Tree:",1-accuracy_score(y_train, y_pred))
	print("Classification Report : ")
    print(classification_report(y_train,y_pred))
    print("Decision_tree:test set")
    y_pred = clf_entropy.predict(X_test)
    print("Decision_tree:Confusion Matrix: \n", confusion_matrix(y_test, y_pred))
    auc1 = multiclass_roc_auc_score(y_test,y_pred)
    print('AUC for Decision Tree:',auc1)
    y_score = clf_entropy.predict_proba(X_test)
    n_classes=3
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    y_test1 = label_binarize(y_test, classes=[0, 1, 2])
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test1[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    colors = list(['blue', 'red', 'green'])
    for i, color in zip(range(n_classes), colors):
        plt.plot(fpr[i], tpr[i], color=color,label='ROC curve of class {0} (area = {1:0.2f})'''.format(i, roc_auc[i]))
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([-0.05, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC-AUC curve')
    plt.legend(loc="lower right")
    plt.show()
    print ("Decision_tree:Accuracy : ", accuracy_score(y_test,y_pred)*100)
    print("Error rate for Decision Tree:",1-accuracy_score(y_test, y_pred))
	print("Classification Report : ")
    print(classification_report(y_test,y_pred))
    return(clf_entropy.predict(fertility_columns_test))

#Random Forest Classification    
def run_randomForests_classification(X_train,X_test,y_train,y_test,fertility_columns_test):
    rf=RandomForestClassifier(n_estimators=200,random_state=39,max_depth=4,oob_score=True)
    rf.fit(X_train,y_train)
    print('Train set')
    y_pred=rf.predict(X_train)
    print("Random Forest:Confusion Matrix: \n", confusion_matrix(y_train, y_pred))
    print("Random Forest OOB error rate :",rf.oob_score_)
    auc1 = multiclass_roc_auc_score(y_train,y_pred)
    print('AUC for random forest:',auc1)
    y_score = rf.predict_proba(X_train)
    n_classes=3
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    y_train1 = label_binarize(y_train, classes=[0, 1, 2])
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_train1[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    colors = list(['blue', 'red', 'green'])
    for i, color in zip(range(n_classes), colors):
        plt.plot(fpr[i], tpr[i], color=color,label='ROC curve of class {0} (area = {1:0.2f})'''.format(i, roc_auc[i]))
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([-0.05, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC-AUC curve')
    plt.legend(loc="lower right")
    plt.show()
    print("Accuracy For Random Forest:",accuracy_score(y_train, y_pred))
    print("Error rate for random forest:",1-accuracy_score(y_train, y_pred))
	print("Classification Report : ")
    print(classification_report(y_train,y_pred))
    print('Test set')
    y_pred=rf.predict(X_test)
    print("Random Forest:Confusion Matrix: \n", confusion_matrix(y_test, y_pred))
    print("Random Forest OOB error rate :",rf.oob_score_)
    auc1 = multiclass_roc_auc_score(y_test,y_pred)
    print('AUC for random forest:',auc1)
    y_score = rf.predict_proba(X_test)
    n_classes=3
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    y_test1 = label_binarize(y_test, classes=[0, 1, 2])
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test1[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    colors = list(['blue', 'red', 'green'])
    for i, color in zip(range(n_classes), colors):
        plt.plot(fpr[i], tpr[i], color=color,label='ROC curve of class {0} (area = {1:0.2f})'''.format(i, roc_auc[i]))
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([-0.05, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC-AUC curve')
    plt.legend(loc="lower right")
    plt.show()
    print("Accuracy For Random Forest:",accuracy_score(y_test, y_pred))
    print("Error rate for random forest:",1-accuracy_score(y_test, y_pred))
	print("Classification Report : ")
    print(classification_report(y_test,y_pred))
    return(rf.predict(fertility_columns_test))
    
#Decision Tree Regression 
def run_decision_tree_regression(X_train,X_test,y_train,y_test,rainfall_column_test):
    clf_entropy = DecisionTreeRegressor(random_state = 100,max_depth = 3, min_samples_leaf = 5) 
    clf_entropy.fit(X_train, y_train)  
    print("Decision_tree:train set")
    y_pred = clf_entropy.predict(X_train)
    print('Decision_Tree Mean squared Error :{}'.format(mean_squared_error(y_train,y_pred)))
    print('Decision_Tree r2_score :{}'.format(r2_score(y_train,y_pred)))
    print('Decision_Tree Error Rate :{}'.format(1-r2_score(y_train,y_pred)))
    print("Decision_tree:test set")
    y_pred = clf_entropy.predict(X_test)
    print('Decision_Tree Mean Squared error :{}'.format(mean_squared_error(y_test,y_pred)))
    print('Decision_Tree r2_score :{}'.format(r2_score(y_test,y_pred)))
    print('Decision_Tree Error Rate :{}'.format(1-r2_score(y_test,y_pred)))     
    return(clf_entropy.predict(rainfall_column_test))
    
#Random Forest Regression
def run_randomForests_regression(X_train,X_test,y_train,y_test,rainfall_column_test):
    rf=RandomForestRegressor(n_estimators=200,random_state=39,max_depth=4)
    rf.fit(X_train,y_train)
    print('Train set')
    y_pred=rf.predict(X_train)
    print('Random Forests Mean squared Error :{}'.format(mean_squared_error(y_train,y_pred)))
    print('Random Forests r2_score :{}'.format(r2_score(y_train,y_pred)))
    print('Random Forest Error Rate :{}'.format(1-r2_score(y_train,y_pred)))
    print('Tesst set')
    y_pred=rf.predict(X_test)
    print('Random Forests Mean Squared error :{}'.format(mean_squared_error(y_test,y_pred)))
    print('Random Forests r2_score :{}'.format(r2_score(y_test,y_pred)))     
    print('Random Forest Error Rate :{}'.format(1-r2_score(y_test,y_pred)))
    return(rf.predict(rainfall_column_test))

#cross validation
from sklearn.model_selection import cross_val_score    

rf=RandomForestClassifier(n_estimators=200,random_state=39,max_depth=4,oob_score=True)    
cross_val_score(rf,fer_X,fer_y, cv=10)

rf=RandomForestRegressor(n_estimators=200,random_state=39,max_depth=4)
cross_val_score(rf,rainfall_X,rainfall_y, cv=10)

clf_entropy = DecisionTreeClassifier(criterion = "entropy", random_state = 100,max_depth = 3, min_samples_leaf = 5) 
cross_val_score(clf_entropy,fer_X,fer_y, cv=10)

clf_entropy = DecisionTreeRegressor(random_state = 100,max_depth = 3, min_samples_leaf = 5) 
cross_val_score(clf_entropy,rainfall_X,rainfall_y, cv=10)
    
list_fertility_columns=[]
N=int(input("Enter value of N : "))
list_fertility_columns.append(N)
P=float(input("Enter value of P : "))
list_fertility_columns.append(P)
K=float(input("Enter value of K : "))
list_fertility_columns.append(K)
ph=float(input("Enter value of ph : "))
list_fertility_columns.append(ph)
ec=float(input("Enter value of ec : "))
list_fertility_columns.append(ec)
fertility_columns_test=pd.DataFrame([list_fertility_columns],columns = ['N','P','K','ph','ec'])

district=input("Enter value of Disctrict : ")
year=int(input("Enter value of year : "))
month=input("Enter value of month : ")

cols=rainfall_X.columns
cols=cols[1:]
rainfall_column_test = []
rainfall_column_test.append(year)
for i in cols:
    if i.split("_")[1]==month or i.split("_")[1]==district:
        rainfall_column_test.append(1)
    else:    
        rainfall_column_test.append(0)
 
rainfall_column_test=pd.DataFrame([rainfall_column_test],columns = rainfall_X.columns)
              
#classification using random forest and then regression using randomforest
predicted_fertility=run_randomForests_classification(X_fer_train, X_fer_test, y_fer_train, y_fer_test,fertility_columns_test)    
predicted_rainfall=run_randomForests_regression(X_rainfall_train, X_rainfall_test, y_rainfall_train, y_rainfall_test,rainfall_column_test)
print("Predicted Values Using Random Forest as Classification and Random Forest Regression : \n")
print("Predicted Fertility using random forest classification : \n",predicted_fertility)
print("Predicited rainfall using random forest regression : \n",predicted_rainfall)

crop=[]

for i in range(0,len(cropdb)):
    if((predicted_rainfall >= cropdb['min_rainfall'][i] and predicted_rainfall < cropdb['max_rainfall'][i]) and predicted_fertility == cropdb['fertility'][i]) :
        #print(cropdb['crop'][i],"\n")
        cr=cropdb['crop'][i]
        if ( len(crop)==0):
             crop.insert(0,cr)
        else:
             crop.append(cr)

class MainWindow(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self.panel = wx.Panel(self)

        self.list = wx.ListCtrl(self.panel, style=wx.LC_REPORT)
        self.list.InsertColumn(0, "Crop Names")
        

        for a in range(len(crop)):        
            self.list.Append([ crop[a]])

        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.list, proportion=1, flag=wx.EXPAND)

        self.panel.SetSizerAndFit(self.sizer)
        self.Show()

        # Save
        #for row in range(self.list.GetItemCount()):
            #print(", ".join([self.list.GetItem(row, col).GetText() for col in range(self.list.GetColumnCount())]))

app = wx.App(False)
win = MainWindow(None)
app.MainLoop()
        

        
    












    