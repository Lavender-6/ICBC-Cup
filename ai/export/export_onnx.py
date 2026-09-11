import torch
import onnx
from train.train_classifier import SignalClassifier, MODULATIONS
from train.train_regressor import SNRRegressor


def export_classifier(model_path: str = "models/classifier.pth", output_path: str = "models/classifier.onnx"):
    model = SignalClassifier(num_classes=len(MODULATIONS))
    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()

    dummy_input = torch.randn(1, 1, 64, 64)
    torch.onnx.export(
        model,
        dummy_input,
        output_path,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={"input": {0: "batch"}, "output": {0: "batch"}},
        opset_version=14,
    )
    onnx.checker.check_model(onnx.load(output_path))
    print(f"Classifier exported to {output_path}")


def export_regressor(model_path: str = "models/regressor.pth", output_path: str = "models/regressor.onnx"):
    model = SNRRegressor()
    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()

    dummy_input = torch.randn(1, 1, 64, 64)
    torch.onnx.export(
        model,
        dummy_input,
        output_path,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={"input": {0: "batch"}, "output": {0: "batch"}},
        opset_version=14,
    )
    onnx.checker.check_model(onnx.load(output_path))
    print(f"Regressor exported to {output_path}")


if __name__ == "__main__":
    export_classifier()
    export_regressor()
