import logging


class PersuasionModel(object):
    def _clean_input(self, input_file):
        # clean input file
        print('cleaning')
        return input_file

    def get_tag(self, input_file):
        cleaned_input = self._clean_input(input_file)
