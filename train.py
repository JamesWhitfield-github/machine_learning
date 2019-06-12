{\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;\red208\green38\blue12;\red255\green255\blue255;\red77\green80\blue85;
\red0\green0\blue0;\red127\green11\blue224;\red74\green29\blue161;\red23\green95\blue199;\red15\green116\blue100;
\red89\green59\blue50;}
{\*\expandedcolortbl;;\cssrgb\c85882\c23137\c3922;\cssrgb\c100000\c100000\c100000;\cssrgb\c37255\c38824\c40784;
\cssrgb\c0\c0\c0;\cssrgb\c57647\c20392\c90196;\cssrgb\c36863\c20784\c69412;\cssrgb\c9804\c46275\c82353;\cssrgb\c0\c52157\c46667;
\cssrgb\c42745\c29804\c25490;}
\paperw11900\paperh16840\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs24 \cf2 \cb3 \expnd0\expndtw0\kerning0
"""\cf4 \
\cf2 Usage:\cf4 \
\cf2     python3 train.py <initials> [options]\cf4 \
\
\cf2 Options:\cf4 \
\cf2     --dim=<k>           dimension of the feature space for approximate rbf kernel\cf4 \
\cf2     --std=<sd>          standard deviation of rbf kernel\cf4 \
\cf2     --epochs=<n>        number of epochs to train for [default: 1]\cf4 \
\cf2     --lr=<lr>           learning rate while training [default: 0.001]\cf4 \
\cf2 """\cf4 \
\
\cf6 import\cf4  tensorflow \cf6 as\cf4  tf\
\cf6 import\cf4  argparse\
\
\cf6 from\cf4  \cf7 input\cf4  \cf6 import\cf4  make_columns, train_input_fn, ml_engine_online_serving_input_receiver_fn\
\cf6 from\cf4  model \cf6 import\cf4  KernelRegressionModelFn\
\
DATA_PATH = \cf2 'gs://datatonic-telecom-data/dataset/*.csv'\cf4 \
MODEL_BUCKET = \cf2 'gs://datatonic-telecom-models/'\cf4 \
\
\
\cf6 def\cf4  \cf8 get_args\cf4 ():\
    \cf2 """Get command line arguments."""\cf4 \
    parser = argparse.ArgumentParser()\
\
    parser.add_argument(\cf2 'initials'\cf4 , \cf7 type\cf4 =\cf7 str\cf4 )\
\
    parser.add_argument(\cf2 '--dim'\cf4 , \cf7 type\cf4 =\cf7 int\cf4 , default=\cf9 20\cf4 )\
\
    parser.add_argument(\cf2 '--std'\cf4 , \cf7 type\cf4 =\cf7 int\cf4 , default=\cf9 1\cf4 )\
\
    parser.add_argument(\cf2 '--epochs'\cf4 , \cf7 type\cf4 =\cf7 int\cf4 , default=\cf9 100\cf4 )\
\
    parser.add_argument(\cf2 '--lr'\cf4 , \cf7 type\cf4 =\cf7 float\cf4 , default=\cf9 0.00001\cf4 )\
\
    \cf6 return\cf4  parser.parse_args()\
\
\
\cf6 def\cf4  \cf8 main\cf4 (FLAGS):\
\
    dense_columns, sparse_columns = make_columns()\
\
    \cf10 # make matrix factorization estimator\cf4 \
    model_fn = KernelRegressionModelFn(dense_columns, sparse_columns, FLAGS.dim, FLAGS.std, FLAGS.lr)\
\
    estimator = tf.estimator.Estimator(\
        model_fn,\
        model_dir=MODEL_BUCKET+FLAGS.initials+\cf2 '/model'\cf4 \
    )\
\
    \cf10 # train\cf4 \
    input_fn = train_input_fn(DATA_PATH, FLAGS.epochs)\
    estimator.train(input_fn)\
\
    \cf10 # export model for serving\cf4 \
    SIRfn = ml_engine_online_serving_input_receiver_fn()\
\
    estimator.export_savedmodel(\
        export_dir_base=MODEL_BUCKET+FLAGS.initials+\cf2 '/serving'\cf4 ,\
        serving_input_receiver_fn=SIRfn\
    )\
\
\
\cf6 if\cf4  __name__ == \cf2 '__main__'\cf4 :\
    main(FLAGS = get_args())\
\pard\pardeftab720\partightenfactor0
\cf0 \cb1 \
\
}