import tensorflow as tf
import numpy as np
from db_utils import *

track_own_tags = get_track_own_tags()
track_artist_tags = get_track_artist_tags()
track_album_tags = get_track_album_tags()

# Remove irrelevant tags
track_own_tags = track_own_tags[['track' not in t for t in track_own_tags.tag]]
track_album_tags = track_album_tags[['album' not in t for t in track_album_tags.tag]]
track_artist_tags = track_artist_tags[['artist' not in t for t in track_artist_tags.tag]]

# Remove tags with just one track
track_own_tags = track_own_tags[track_own_tags.groupby('tag').tag.transform('count') > 1]
track_album_tags = track_album_tags[track_album_tags.groupby('tag').tag.transform('count') > 1]
track_artist_tags = track_artist_tags[track_artist_tags.groupby('tag').tag.transform('count') > 1]

# Merge tags not in set by priority -> track > album > artist
new_tracks_album = track_album_tags.loc[~track_album_tags.track_id.isin(track_own_tags.track_id)]
raw_track_tags = pd.concat([track_own_tags, new_tracks_album])

new_tracks_artist = track_artist_tags.loc[~track_artist_tags.track_id.isin(raw_track_tags.track_id)]
raw_track_tags = pd.concat([raw_track_tags, new_tracks_artist]).reset_index(drop=True)

print(f"Unique tracks: {len(raw_track_tags.track_id.unique())}")

# Strip spaces and multiply words depending on rank
track_tags = raw_track_tags.copy()
track_tags['tag'] = track_tags['tag'].apply(lambda x: x.replace(' ', ''))
track_tags = track_tags.loc[track_tags.index.repeat(track_tags['rank'].apply(lambda x: 11 - x))]

# Group by track id and aggregate into lists
grouped_tags = track_tags.groupby(track_tags['track_id'])['tag'].apply(list).reset_index(name='tags')

# Create soup of words for each track
grouped_tags['tags'] = grouped_tags['tags'].apply(lambda x: ' '.join(x))

# Create the layer.
vectorize_layer = tf.keras.layers.TextVectorization(output_mode='tf_idf')

# Now that the vocab layer has been created, call `adapt` on the
# text-only dataset to create the vocabulary. You don't have to batch,
# but for large datasets this means we're not keeping spare copies of
# the dataset.
vectorize_layer.adapt(grouped_tags['tags'].values)

# Create the model that uses the vectorize text layer
model = tf.keras.models.Sequential()

# Start by creating an explicit input layer. It needs to have a shape of
# (1,) (because we need to guarantee that there is exactly one string
# input per batch), and the dtype needs to be 'string'.
model.add(tf.keras.Input(shape=(1,), dtype=tf.string))

# The first layer in our model is the vectorization layer. After this
# layer, we have a tensor of shape (batch_size, max_len) containing
# vocab indices.
model.add(vectorize_layer)

# Now, the model can map strings to integers, and you can add an
# embedding layer to map these integers to learned embeddings.
text_matrix = model.predict([grouped_tags['tags'].values])
print(text_matrix)
text_matrix = text_matrix[np.newaxis, :]

# Cosine similarity
cosine_sim = tf.keras.layers.Dot(axes=(2, 2), normalize=True)
d = cosine_sim([text_matrix, text_matrix])

print(d)
