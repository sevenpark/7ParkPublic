class AlgorithmArnProvider:

    @staticmethod
    def get_algorithm_arn(current_region):
        mapping = {
            "us-east-2": "arn:aws:sagemaker:us-east-2:084888172679:algorithm/stopword-2020-02-13-2",
        }
        return mapping[current_region]
