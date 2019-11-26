class ModelPackageArnProvider:

    @staticmethod
    def get_model_package_arn(current_region):
        mapping = {
            "us-east-2": "arn:aws:sagemaker:us-east-2:084888172679:model-package/ner-cc-txns-2019-11-22-14-58-36-327",
        }
        return mapping[current_region]
