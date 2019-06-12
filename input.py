{\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;\red127\green11\blue224;\red255\green255\blue255;\red77\green80\blue85;
\red0\green0\blue0;\red74\green29\blue161;\red208\green38\blue12;\red15\green116\blue100;\red23\green95\blue199;
\red89\green59\blue50;}
{\*\expandedcolortbl;;\cssrgb\c57647\c20392\c90196;\cssrgb\c100000\c100000\c100000;\cssrgb\c37255\c38824\c40784;
\cssrgb\c0\c0\c0;\cssrgb\c36863\c20784\c69412;\cssrgb\c85882\c23137\c3922;\cssrgb\c0\c52157\c46667;\cssrgb\c9804\c46275\c82353;
\cssrgb\c42745\c29804\c25490;}
\paperw11900\paperh16840\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs24 \cf2 \cb3 \expnd0\expndtw0\kerning0
import\cf4  numpy \cf2 as\cf4  np\
\cf2 import\cf4  tensorflow \cf2 as\cf4  tf\
\cf2 from\cf4  collections \cf2 import\cf4  OrderedDict\
\
\
VOCABULARIES = \cf6 dict\cf4 (\
    area=[\
        \cf7 'SOUTH FLORIDA AREA'\cf4 ,\
        \cf7 'NEW ENGLAND AREA'\cf4 ,\
        \cf7 'MIDWEST AREA'\cf4 ,\
        \cf7 'DC/MARYLAND/VIRGINIA AREA'\cf4 ,\
        \cf7 'OHIO AREA'\cf4 ,\
        \cf7 'LOS ANGELES AREA'\cf4 ,\
        \cf7 'GREAT LAKES AREA'\cf4 ,\
        \cf7 'HOUSTON AREA'\cf4 ,\
        \cf7 'CALIFORNIA NORTH AREA'\cf4 ,\
        \cf7 'CENTRAL/SOUTH TEXAS AREA'\cf4 ,\
        \cf7 'TENNESSEE AREA'\cf4 ,\
        \cf7 'ATLANTIC SOUTH AREA'\cf4 ,\
        \cf7 'NEW YORK CITY AREA'\cf4 ,\
        \cf7 'PHILADELPHIA AREA'\cf4 ,\
        \cf7 'CHICAGO AREA'\cf4 ,\
        \cf7 'NORTH FLORIDA AREA'\cf4 ,\
        \cf7 'DALLAS AREA'\cf4 ,\
        \cf7 'NORTHWEST/ROCKY MOUNTAIN AREA'\cf4 ,\
        \cf7 'SOUTHWEST AREA'\cf4 \
    ],\
    new_user=[\cf7 'U'\cf4 , \cf7 'N'\cf4 , \cf7 'Y'\cf4 ],\
    refurb_or_new=[\cf7 'R'\cf4 ,\cf7 'N'\cf4 ],\
    dualband=[\cf7 'U'\cf4 , \cf7 'N'\cf4 , \cf7 'Y'\cf4 ],\
    web_capable=[\cf7 'WC'\cf4 , \cf7 'UNKW'\cf4 , \cf7 'WCMB'\cf4 , \cf7 'NA'\cf4 ],\
    manual_limit=[\cf7 'false'\cf4 , \cf7 'true'\cf4 ],\
    PRIZM_code=[\cf7 'U'\cf4 , \cf7 'C'\cf4 , \cf7 'T'\cf4 , \cf7 'S'\cf4 , \cf7 'R'\cf4 ],\
    credit_card=[\cf7 'false'\cf4 , \cf7 'true'\cf4 ],\
    cred_score=[ \cf7 'AA'\cf4 , \cf7 'A'\cf4 , \cf7 'BA'\cf4 , \cf7 'B'\cf4 , \cf7 'CA'\cf4 , \cf7 'C'\cf4 , \cf7 'DA'\cf4 , \cf7 'D'\cf4 , \cf7 'EA'\cf4 , \cf7 'E'\cf4 ],\
    churn=[\cf8 0\cf4 , \cf8 1\cf4 ]\
)\
\
\
SCHEMA = [\
    \cf7 'Customer_ID'\cf4 ,\cf7 'area'\cf4 ,\cf7 'user_months'\cf4 ,\cf7 'new_user'\cf4 ,\cf7 'phones_used'\cf4 , \cf7 'models_used'\cf4 ,\
    \cf7 'handset_price'\cf4 ,\cf7 'handset_age'\cf4 ,\cf7 'refurb_or_new'\cf4 ,\cf7 'dualband'\cf4 ,\cf7 'web_capable'\cf4 ,\
    \cf7 'manual_limit'\cf4 ,\cf7 'PRIZM_code'\cf4 ,\cf7 'credit_card'\cf4 ,\cf7 'cred_score'\cf4 ,\cf7 'churn'\cf4 \
]\
\
DEFAULTS = [\cf8 0\cf4 ,\cf7 ''\cf4 ,\cf8 0\cf4 ,\cf7 ''\cf4 ,\cf8 0\cf4 ,\cf8 0\cf4 ,\cf8 0.0\cf4 ,\cf8 0\cf4 ,\cf7 ''\cf4 ,\cf7 ''\cf4 ,\cf7 ''\cf4 ,\cf7 ''\cf4 ,\cf7 ''\cf4 ,\cf7 ''\cf4 ,\cf7 ''\cf4 ,\cf8 0\cf4 ]\
\
\
\cf2 def\cf4  \cf9 vocab_column\cf4 (key):\
    \cf2 return\cf4  tf.feature_column.categorical_column_with_vocabulary_list(key, VOCABULARIES[key])\
\
\
\cf2 def\cf4  \cf9 make_columns\cf4 ():\
    dense_columns = []\
    sparse_columns = []\
\
    \cf2 for\cf4  x \cf2 in\cf4  (\cf7 'user_months'\cf4 , \cf7 'phones_used'\cf4 , \cf7 'models_used'\cf4 , \cf7 'handset_price'\cf4 , \cf7 'handset_age'\cf4 ):\
        column = tf.feature_column.numeric_column(x)\
        dense_columns.append(column)\
\
    \cf2 for\cf4  x \cf2 in\cf4  (\cf7 'area'\cf4 , \cf7 'new_user'\cf4 , \cf7 'refurb_or_new'\cf4 , \cf7 'dualband'\cf4 , \cf7 'web_capable'\cf4 ,\
              \cf7 'manual_limit'\cf4 , \cf7 'PRIZM_code'\cf4 , \cf7 'credit_card'\cf4 ):\
        column = vocab_column(x)\
        sparse_columns.append(column)\
\
    dense_columns.append(tf.feature_column.embedding_column(vocab_column(\cf7 'cred_score'\cf4 ), dimension=\cf8 1\cf4 ))\
\
    \cf10 #churn_column = vocab_column('churn')\cf4 \
\
    \cf2 return\cf4  dense_columns, sparse_columns\
\
\
\cf2 def\cf4  \cf9 parse_csv\cf4 (records):\
    \cf7 """Parse csv row strings into feature tensors."""\cf4 \
\
    tensors = tf.decode_csv(records, record_defaults=DEFAULTS)\
\
    features = \cf6 dict\cf4 (\cf6 zip\cf4 (SCHEMA, tensors))\
    labels = features.pop(\cf7 'churn'\cf4 )\
\
    \cf2 return\cf4  features, labels\
\
\
\cf2 def\cf4  \cf9 train_input_fn\cf4 (path, epochs):\
\
    \cf2 def\cf4  \cf9 input_fn\cf4 ():\
\
        \cf10 # get filenames and shuffle them\cf4 \
        file_list = tf.gfile.Glob(path)\
        dataset = tf.data.Dataset.from_tensor_slices(file_list)\
        dataset = dataset.shuffle(\cf8 50\cf4 )\
\
        \cf10 # read lines of files as row strings, then shuffle and batch\cf4 \
        f = \cf2 lambda\cf4  filepath: tf.data.TextLineDataset(filepath).skip(\cf8 1\cf4 )\
        dataset = dataset.interleave(f, cycle_length=\cf8 8\cf4 , block_length=\cf8 8\cf4 )\
        dataset = dataset.shuffle(\cf8 100000\cf4 )\
        dataset = dataset.batch(\cf8 1000\cf4 )\
\
        \cf10 # parse row strings into features and labels, then return batches\cf4 \
        dataset = dataset.map(parse_csv, num_parallel_calls=\cf8 4\cf4 )\
        dataset = dataset.cache()\
        iterator = dataset.repeat(epochs).make_one_shot_iterator()\
        features, labels = iterator.get_next()\
\
        \cf2 return\cf4  features, labels\
\
    \cf2 return\cf4  input_fn\
\
\
\cf2 def\cf4  \cf9 ml_engine_online_serving_input_receiver_fn\cf4 ():\
\
    features = \{key:tf.placeholder(shape=[\cf2 None\cf4 ], dtype=tf.as_dtype(np.dtype(\cf6 type\cf4 (value))))\
                \cf2 for\cf4  key, value \cf2 in\cf4  \cf6 zip\cf4 (SCHEMA, DEFAULTS)\}\
\
    \cf10 # remove the columns that weren't model inputs\cf4 \
    features.pop(\cf7 'Customer_ID'\cf4 )\
    features.pop(\cf7 'churn'\cf4 )\
\
    fn = tf.estimator.export.build_raw_serving_input_receiver_fn(features)\
\
    \cf2 return\cf4  fn}