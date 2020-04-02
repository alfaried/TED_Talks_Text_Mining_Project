import gensim
import os

class LDA_Mallet:
    # Initialize class method
    def __init__(self, mallet_path):
        self.lda_models_folder = "LDA_Module/models/"
        self.mallet_path = mallet_path
        self.lda_mallet_model = None


    # SETTER Methods
    def update_models_folder_path(self, path):
        if path == None:
            raise Exception("path is required")
        
        self.lda_models_folder = path 

    def update_mallet_path(self, path):
        if path == None:
            raise Exception("path is required")
        
        self.mallet_path = path

    def set_model(self, lda_model):
        if lda_model == None:
            raise Exception("lda_model is required")

        self.lda_mallet_model = lda_model
    
    def train_model(self, vecs, num_topics, dictionary):
        if vecs == None:
            raise Exception("corpus required")

        if num_topics == None:
            raise Exception("num_topics required")

        if dictionary == None:
            raise Exception("dictionary required")
        
        model = gensim.models.wrappers.LdaMallet(self.get_mallet_path(), corpus=vecs, num_topics=num_topics, id2word=dictionary)
        self.set_model(model)
        return model

    
    # GETTER Methods
    def get_model_folder_path(self):
        return self.lda_models_folder

    def get_mallet_path(self):
        return self.mallet_path

    def get_model(self):
        if self.lda_mallet_model == None:
            raise Exception("Please train a model first or get one of the pretrained model")

        return self.lda_mallet_model

    def get_pretrained_model(self, model_name="train_lda_48"):
        if len(os.listdir(self.lda_models_folder)) == 0:
            raise Exception("No pretrained models. Please train a model first")
        
        model = gensim.models.wrappers.LdaMallet.load(self.get_model_folder_path() + model_name)
        self.set_model(model)
        return model


    # The following methods works only after you've set the LDA model for this class
    def save_trained_model(self, model_name):
        if model_name == None:
            raise Exception("model_name required")
        
        model = self.get_model()
        model.save(self.get_model_folder_path() + model_name)

        return model

    def predict_topics_for_vec(self, vec):
        if vec == None:
            raise Exception("vec required")
        
        model = self.get_model()
        topic_distribution = model[vec]
        return sorted(topic_distribution, key=lambda x: (x[1]), reverse=True)

    def predict_topics_for_vecs(self, vecs):
        if vecs == None:
            raise Exception("vecs required")
        
        model = self.get_model()
        topic_distirbution_list = []

        for index, topic_distribution in enumerate(model[vecs]):
            topic_distirbution_list.append(sorted(topic_distribution, key=lambda x: (x[1]), reverse=True))

        return topic_distirbution_list

    def get_dominant_topic_for_vec(self, topic_distribution):
        if topic_distribution == None:
            raise Exception("topic_distribution required")
        
        model = self.get_model()
        topic_id, topic_probability = topic_distribution[0]
        word_distribution = model.show_topic(topic_id)
        topic_keywords = ", ".join([word for word, prob in word_distribution])

        return topic_id, topic_probability, topic_keywords

    def get_dominant_topic_for_vecs(self, topic_distribution_list):
        if topic_distribution_list == None:
            raise Exception("topic_distribution_list required")
        
        dominant_topic_list = []

        for topic_distribution in topic_distribution_list:
            dominant_topic_list.append(self.get_dominant_topic_for_vec(topic_distribution))

        return dominant_topic_list

    # def cluster