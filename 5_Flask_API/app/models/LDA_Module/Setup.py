from LDA_Module import LDA, Preprocess

import os

# Run this method once to set up pretrained model and dictionary
def auto_setup(mallet_path):
    if mallet_path == None:
        raise Exception("mallet_path is required")

    train_folder_path = "LDA_Module/reference_data/train_data/"

    # Initialize class
    train_dataset = Preprocess.Dataset(train_folder_path, "train")

    # Get required data from object and save dictionary
    train_corpus = train_dataset.get_corpus()
    train_vecs = train_dataset.get_vecs()
    train_dictionary = train_dataset.get_dictionary()

    # Train and save model
    lda_obj = LDA.LDA_Mallet(mallet_path)
    lda_obj.train_model(train_vecs, 48, train_dictionary)
    lda_obj.save_trained_model("train_model_48")

    # Find dominant topics of the training dataset
    topic_distribution_list = lda_obj.predict_topics_for_vecs(train_vecs)
    dominant_topics_list = lda_obj.get_dominant_topic_for_vecs(topic_distribution_list)

    # Cluster trainscript based on dominant topic
    print("Clustering data..")
    clustered_data = {}
    fids = train_corpus.fileids()
    for index in range(0, len(fids)):
        transcript_id = fids[index]
        dominant_topic = dominant_topics_list[index]
        try:
            clustered_data[dominant_topic[0]].append(transcript_id) 
        except:
            clustered_data[dominant_topic[0]] = [transcript_id]

    # Write cluster to the reference data file
    print("Writing data..")
    clustered_folder_path = "LDA_Module/reference_data/clustered_data/"
    for topic_id, transcript_list in clustered_data.items():
        cluster_folder_name = clustered_folder_path +  str(topic_id)

        if not os.path.exists(cluster_folder_name):
            os.mkdir(cluster_folder_name)

        for transcript in transcript_list:
            transcript_path = cluster_folder_name + "/" + transcript
            transcript_file = open(transcript_path, "w")
            transcript_file.writelines(train_corpus.raw(transcript))

def upload_transcript(file_path, mallet_path):
    return_hash = {}

    test_dataset = Preprocess.Dataset(file_path, "test")
    vec = test_dataset.get_vec()

    lda_obj = LDA.LDA_Mallet(mallet_path)
    lda_obj.get_pretrained_model()

    topic_distribution = lda_obj.predict_topics_for_vec(vec)
    dominant_topic = lda_obj.get_dominant_topic_for_vec(topic_distribution)

    transcript_id_list = lda_obj.retrieve_related_transcript_id(int(dominant_topic[0]))

    return_hash["Topic No."] = dominant_topic[0]
    return_hash["Topic Prob."] = dominant_topic[1]
    return_hash["Topic Keywords."] = dominant_topic[2]
    return_hash["Related Documents"] = transcript_id_list

    return return_hash