## [1.0.4] - 2022-03-22
### Changed
- Fix `ImageReader` to work either with image path or `np.ndarray`
- Added `metadata` support to `callbacks/tf2onnx` when converting to onnx format


## [1.0.3] - 2022-03-20
### Changed
- Changed `mltu.augmentors` to work only with `Image` objects

### Added
- Created `Image` object in `mltu.annotations.image` to handle image annotations


## [1.0.2] - 2022-03-20
### Changed
- changes `OnnxInferenceModel` in `mltu.torch.inferenceModels` to load custom metadata from saved ONNX model
- improved `mltu.dataProvider` to remove bad samples from dataset on epoch end

### Added:
- added `mltu.torch.losses`, used to create PyTorch losses, that may be used in training and validation
- added CTC loss to `mltu.torch.losses` that can be used for training CTC based models
- added `Model2onnx` and `Tensorboard` callbacks to `mltu.torch.callbacks`, used to create PyTorch callbacks, that may be used in training and validation
- added `CERMetric` and `WERMetric` to `mltu.torch.metrics`, used to create PyTorch metrics, that may be used in training and validation
- created 08 pytorch tutorial, that shows how to use `mltu.torch` to train CTC based models


## [1.0.1] - 2022-03-06
### Changed
- In all tutorials removed stow dependency and replaced with os package, to make it easier to use on Windows 11

### Added:
- added `mltu.torch`, that contains PyTorch utilities for training machine learning models
- added `mltu.torch.dataProvider`, used to create PyTorch data loaders for training and validation
- added `mltu.torch.models`, used to create PyTorch models, that wrapps whole model pipeline (training, validation, metrics, callbacks, etc.)
- added `mltu.torch.callbacks`, used to create PyTorch callbacks, that may be used in training and validation
- added `mltu.torch.metrics`, used to create PyTorch metrics, that may be used in training and validation
- added `07_pytorch_tutorial` tutorial


## [1.0.0] - 2022-03-06
### Changed
- detaching TensorFlow from mltu, now mltu is only a collection of utilities for training machine learning models

### Added:
- added 06_pytorch_introduction tutorial
- added `mltu.tensorflow` and `mltu.torch` into built package


## [0.1.6] - 2022-02-26
### Changed
- 
### Added:
- added 05_sound_to_text tutorial
- added `WavReader` to `mltu/preprocessors`, used to read wav files and convert them to numpy arrays


## [0.1.7] - 2022-02-03
### Changed
- added `mltu.utils` into built package


## [0.1.5] - 2022-01-10
### Changed
- seperated `CWERMetric` to `CER` and `WER` Metrics in `mltu.metrics`, Character/word rate was calculatted in a wrong way
- created @setter for augmentors and transformers in DataProvider, to properlly add augmentors and transformers to the pipeline
- augmentors and transformers must inherit from `mltu.augmentors.base.Augmentor` and `mltu.transformers.base.Transformer` respectively
- updated ImageShowCV2 transformer documentation
- fixed OnnxInferenceModel in `mltu.inferenceModels` to use CPU even if GPU is available with force_cpu=True flag

### Added:
- added RandomSharpen to mltu.augmentors, used for simple image augmentation;
- added ImageShowCV2 to mltu.transformers, used to show image with cv2 for debugging purposes;
- added better explained documentation
- created unittests for CER and WER in mltu.utils.text_utils and TensorFlow verion of CER and WER mltu.metrics


## [0.1.4] - 2022-12-21
### Added:
- added mltu.augmentors (RandomBrightness, RandomRotate, RandomErodeDilate) - used for simple image augmentation;


## [0.1.3] - 2022-12-20

Initial release of mltu (Machine Learning Training Utilities)

- Project to help with training machine learning models