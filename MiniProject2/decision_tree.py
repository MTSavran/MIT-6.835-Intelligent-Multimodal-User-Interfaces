import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import accuracy_score

from normalize_frames import normalize_frames
from load_gestures import load_gestures


joints = ['head', 'neck', 'left_shoulder', 'left_elbow', 'left_hand', 'right_shoulder', 'right_elbow', 'right_hand', 'torso', 'left_hip', 'right_hip']
dims = ['x', 'y', 'z']

# remove truncation of numpy array printing
np.set_printoptions(threshold=np.nan)

# properties
num_frames = 36
ratio = 0.9

# 6. FORMAT DATA
gesture_sets = load_gestures()
gesture_sets = normalize_frames(gesture_sets, num_frames)

samples, labels = [], []

for gs in gesture_sets:
    for seq in gs.sequences:
        sample = np.concatenate(list(map(lambda x: x.frame, seq.frames)))
        samples.append(sample)
        labels.append(int(gs.label))

for ratio in [0.1,0.4,0.7,0.9]:
    train_total, test_total = 0,0
    for trial in range(5):
        X, Y = np.vstack(samples), np.array(labels)
        print (X.shape)
        print (Y.shape)
        X_train, X_test, y_train, y_test = train_test_split(X, Y, train_size=ratio, random_state=10)

        # 7. CREATE AND TRAIN MODEL

        clf = DecisionTreeClassifier(criterion='gini')

        clf.fit(X_train, y_train)
        # print("num features: ", clf.feature_importances_.size)

        # 7. TEST MODEL

        y_train_pred = clf.predict(X_train)
        train_accuracy = accuracy_score(y_train, y_train_pred) * 100
        # print("train_accuracy", train_accuracy)

        y_test_pred = clf.predict(X_test)
        test_accuracy = accuracy_score(y_test,y_test_pred) * 100
        # print("test_accuracy", test_accuracy)

        train_total += train_accuracy
        test_total += test_accuracy
    print ("Ratio is: ", ratio)
    print ("Average train acc: ", train_total/5.0)
    print ("Average train acc: ", test_total/5.0)


# 8. VISUALIZE MODEL
feature_names = ['frame ' + str(i)+' - '+str(joints[i%11])+' - '+str(dims[i%3]) for i in range(33*num_frames)]

dot_data = export_graphviz(
    clf,
    out_file='tree.dot',
    feature_names=feature_names,
    class_names=["pan left", "pan right", "pan up", "pan down", "zoom in", "zoom out", "rotate clockwise", "rotate counterclockwise", "point"],
    filled=True,
    rounded=True,
    special_characters=True
)
