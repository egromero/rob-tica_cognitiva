##!
import AsaUtils

import numpy as np
from sklearn import svm
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

#Section 0. Define Path to seek features
RootDescPath='MIT-10-DescriptorsPath'

#Section 1. Define classifiers to use in this activity
classifiersDefs = {'SVM':"svm.LinearSVC(penalty='l2', loss='squared_hinge', dual=True, tol=0.0001, C=1.0, multi_class='ovr')"}

#Section 2. main options
options = {'DescriptorsPath':'../Scenes-15-Classes/Feats/'}
options['DescriptorSize'] = 4096
 
#Section 3. Read training data
descriptorsPath=options['DescriptorsPath'] + 'TrainSet'
classNames,trainFeats,trainLabels=AsaUtils.getMatlabDescriptors(descriptorsPath, 'mat',4096)

#Section 4. Train Classifier
print('******Training classifier, it can take time !, be patient !')
classifier = eval(classifiersDefs['SVM'])

classifier.fit(trainFeats,trainLabels)
    
#Section 5. Read test data
descriptorsPath=options['DescriptorsPath'] + 'TestSet'
classNames,testFeats,testLabels=AsaUtils.getMatlabDescriptors(descriptorsPath, 'mat',4096)

#Section 6. Apply Classifier to test data and calculate accuracy 
print('******Testing classifier, it can take time !, be patient !')
predictedLabels=classifier.predict(testFeats)
accuracy=accuracy_score(testLabels, predictedLabels)
print 'Classification accuracy on test set: ' + str(100*round(accuracy,2)) + '%'

#Section 7. Apply Classifier to train data and calculate accuracy 
predictedTrainLabels=classifier.predict(trainFeats)
accuracy=accuracy_score(trainLabels, predictedTrainLabels)
print 'Classification accuracy on training set: ' + str(100*round(accuracy,2)) + '%'


#Section 8. Computer and show confusion matrix on test set
cnf_matrix = confusion_matrix(testLabels, predictedLabels)
np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
plt.figure()
AsaUtils.plot_confusion_matrix(cnf_matrix, classes=range(1,len(classNames)+1),
                       title='Confusion matrix, without normalization')
 
#Plot normalized confusion matrix
plt.figure()
AsaUtils.plot_confusion_matrix(cnf_matrix, classes=range(1,len(classNames)+1), normalize=True,
                       title='Normalized confusion matrix')
 
plt.show()


    
    



    
    
