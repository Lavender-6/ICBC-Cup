# AI 数据目录

## 数据集

### RadioML 2018.01a (DeepSig)

- 官方地址: https://www.deepsig.ai/datasets/
- 格式: HDF5 (.h5)
- 包含 24 种调制方式，SNR 范围 -20dB ~ +30dB
- 每种调制方式 × 每个 SNR 有 4096 个样本

## 目录结构

```
data/
├── raw/            # 原始下载的数据集（.gitignore 忽略）
├── processed/      # 预处理后的训练数据（.gitignore 忽略）
└── README.md       # 本文件
```

## 数据预处理

1. 下载 RadioML 2018.01a 数据集
2. 将 .h5 文件放入 `raw/` 目录
3. 运行预处理脚本生成频谱图特征：

```bash
cd ai
python -c "
import h5py, numpy as np
from scipy.signal import spectrogram
# TODO: 预处理脚本
"
```
