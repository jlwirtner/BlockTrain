import numpy as np
import pandas as pd
import tensorflow as tf

def get_data():
    train = pd.read_csv('/Users/josh/Downloads/train.csv')
    test = pd.read_csv('/Users/josh/Downloads/test.csv')

    age_norm = (train.Age - train.Age.mean()) / train.Age.std()
    fare_norm = (train.Fare - train.Fare.mean()) / train.Fare.std()

    x_train = pd.DataFrame({'age':age_norm, 'fare':fare_norm, 'survived':train['Survived']})
    x_train = pd.concat([x_train, pd.get_dummies(train.SibSp, prefix='SibSp'), pd.get_dummies(train.Parch, prefix='arch'),  pd.get_dummies(train.Pclass, prefix='Class'), pd.get_dummies(train.Embarked, prefix='Embarked'), pd.get_dummies(train.Sex), pd.get_dummies(train.Cabin, prefix='Cabin')], axis=1)
    x_train.dropna(inplace=True)

    age_norm = (test.Age - train.Age.mean()) / train.Age.std()
    fare_norm = (test.Fare - train.Fare.mean()) / train.Fare.std()
    x_test = pd.DataFrame({'age':age_norm, 'fare':fare_norm})
    x_test = pd.concat([x_test, pd.get_dummies(train.SibSp, prefix='SibSp'), pd.get_dummies(train.Parch, prefix='arch'),  pd.get_dummies(train.Pclass, prefix='Class'), pd.get_dummies(train.Embarked, prefix='Embarked'), pd.get_dummies(train.Sex), pd.get_dummies(train.Cabin, prefix='Cabin')], axis=1)

    y_train = x_train.pop('survived')

    ds = tf.data.Dataset.from_tensor_slices((x_train.values,y_train.values))

    split = int(y_train.shape[0]*0.7)
    train_ds = ds.take(split)
    test_ds  = ds.skip(split)
    train_ds = train_ds.shuffle(len(train)).batch(128)
    test_ds  = test_ds.batch(128)

    return train_ds, test_ds

def get_model(layers, units, alpha=0.001, lambd=0.01):
    tf_layers = []
    # add dense layers w/ L2 regs
    for _ in range(layers):
        tf_layers.append(tf.keras.layers.Dense(units, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(lambd)))
    # output layer
    tf_layers.append(tf.keras.layers.Dense(1, activation='sigmoid'))
    # create model
    model = tf.keras.Sequential(tf_layers)
    # adam == GOD evaluates to True
    adam = tf.keras.optimizers.Adam(
        learning_rate=alpha, beta_1=0.9, beta_2=0.999, epsilon=1e-07, amsgrad=False,
        name='Adam'
    )
    
    model.compile(optimizer=adam,
                 loss=tf.keras.losses.BinaryCrossentropy(from_logits=False),
                 metrics=['accuracy'])
    
    return model
