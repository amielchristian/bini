import transformers
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

directory = "."

model_name = 'FacebookAI/xlm-roberta-base'
train_data = pd.read_csv(f"{directory}/train.csv", encoding='latin-1')
val_data = pd.read_csv(f"{directory}/val.csv", encoding='latin-1')
test_data = pd.read_csv(f"{directory}/test.csv", encoding='latin-1')

def tupleize(data, max_length=512):
    data['safe'] = data['safe'].astype(int)
    tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)

    tokens = tokenizer(list(data["prompt"]), return_tensors="np", padding=True, truncation=True, max_length=max_length)

    token_lengths = [len(token) for token in tokens['input_ids']]
    data_filtered = data.iloc[np.where(np.array(token_lengths) <= max_length)]

    tokens = tokenizer(list(data_filtered["prompt"]), return_tensors="np", padding=True, truncation=True, max_length=max_length)

    labels = np.array(data_filtered["safe"])

    return (tokens, labels)

train_data = tupleize(train_data)
val_data = tupleize(val_data)
test_data = tupleize(test_data)


plt.hist(train_data[1])
plt.hist(val_data[1])
plt.hist(test_data[1])


model = transformers.TFAutoModelForSequenceClassification.from_pretrained(model_name)
model.compile(optimizer=transformers.AdamWeightDecay(learning_rate=3e-5), metrics=['accuracy'])  # No loss argument!

train_input_ids = train_data[0]['input_ids']
train_attention_mask = train_data[0]['attention_mask']
val_input_ids = val_data[0]['input_ids']
val_attention_mask = val_data[0]['attention_mask']

train_input_ids = tf.convert_to_tensor(train_input_ids)
train_attention_mask = tf.convert_to_tensor(train_attention_mask)
val_input_ids = tf.convert_to_tensor(val_input_ids)
val_attention_mask = tf.convert_to_tensor(val_attention_mask)
train_labels = tf.convert_to_tensor(train_data[1])
val_labels = tf.convert_to_tensor(val_data[1])

model.fit(
    x={'input_ids': train_input_ids, 'attention_mask': train_attention_mask},
    y=train_labels,
    validation_data=({'input_ids': val_input_ids, 'attention_mask': val_attention_mask}, val_labels),
    batch_size=8,
    epochs=5
)

model.evaluate(test_data[0], test_data[1])