{\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;\red127\green11\blue224;\red255\green255\blue255;\red77\green80\blue85;
\red0\green0\blue0;\red23\green95\blue199;\red89\green59\blue50;\red74\green29\blue161;\red15\green116\blue100;
}
{\*\expandedcolortbl;;\cssrgb\c57647\c20392\c90196;\cssrgb\c100000\c100000\c100000;\cssrgb\c37255\c38824\c40784;
\cssrgb\c0\c0\c0;\cssrgb\c9804\c46275\c82353;\cssrgb\c42745\c29804\c25490;\cssrgb\c36863\c20784\c69412;\cssrgb\c0\c52157\c46667;
}
\paperw11900\paperh16840\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs24 \cf2 \cb3 \expnd0\expndtw0\kerning0
import\cf4  tensorflow \cf2 as\cf4  tf\
\
\cf2 def\cf4  \cf6 KernelRegressionModelFn\cf4 (dense_columns, sparse_columns, kernel_dim, kernel_std, learning_rate):\
\
    \cf7 # define kernel-approximation feature mapping for numerical data\cf4 \
    rbf_kernel = tf.contrib.kernel_methods.RandomFourierFeatureMapper(\
        input_dim=\cf8 sum\cf4 (x._variable_shape[\cf9 0\cf4 ] \cf2 for\cf4  x \cf2 in\cf4  dense_columns),\
        output_dim=kernel_dim,\
        stddev=kernel_std\
    )\
\
    \cf2 def\cf4  \cf6 model_fn\cf4 (features, labels, mode, config):\
\
        \cf7 # get values from numerical features and transform into rbf features\cf4 \
        dense_input = tf.feature_column.input_layer(features, dense_columns)\
        rbf_features = rbf_kernel.map(dense_input)\
\
        \cf7 # make a linear model from categorical data\cf4 \
        sparse_feature = tf.feature_column.linear_model(features, sparse_columns)\
\
        \cf7 # combining linear layer for output\cf4 \
        X = tf.concat([rbf_features, sparse_feature], axis=-\cf9 1\cf4 )\
        W = tf.Variable(tf.random_normal([kernel_dim + \cf9 1\cf4 , \cf9 1\cf4 ], stddev=\cf9 0.01\cf4 ))\
        b = tf.Variable(tf.random_normal([\cf9 1\cf4 ], stddev=\cf9 0.01\cf4 ))\
        output = tf.matmul(X, W) + b\
\
        \cf7 # define loss and training operations\cf4 \
        head = tf.contrib.estimator.logistic_regression_head()\
        optimizer = tf.train.AdamOptimizer(learning_rate)\
        spec = head.create_estimator_spec(features,\
                                          mode,\
                                          output,\
                                          labels,\
                                          optimizer)\
        \cf2 return\cf4  spec\
\
    \cf2 return\cf4  model_fn\
\pard\pardeftab720\partightenfactor0
\cf0 \cb1 \
\
}