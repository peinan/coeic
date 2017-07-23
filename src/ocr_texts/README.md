# OCR Text

- 画像から文字情報を Google Vision API を使って抽出する
- 入力は基本的には切り出された吹き出しを想定

## 仕様

### ディレクトリ構造
```
sample_data
└── upload_img_01
    ├── balloons      # 吹き出しの画像
    │   ├── 01_01.png
    │   └── 01_02.png
    ├── frames        # コマの画像
    │   ├── 01.png
    │   ├── 02.png
    │   ├── 03.png
    │   ├── 04.png
    │   ├── 05.png
    │   ├── 06.png
    │   └── 07.png
    └── original.png  # アップロードした元イメージ
```

### 入出力フォーマット
```json
extracted_balloons = {
  "upload_img_path": "IMG_PATH",
  "splited_frames": [
    {
      "frame_img": "frame_img_01",
      "extracted_ballonns": [
        "balloon_img1",
        "balloon_img2",
        ...
      ]
    },
    ...
  ]
}
```

### 出力フォーマット
```json
ocr_texts = {
  "upload_img_path": "IMG_PATH",
  "splited_frames": [
    {
      "frame_img": "frame_img_01",
      "extracted_balloons": [
        {
          "balloon_img": "balloon_img1",
          "texts": {
            "text": "serif",
            "position": {
              "left_upper": [x, y],
              "right_bottom": [x, y],
            }
          }
        },
        ...
      ]
    },
    ...
  ]
}
```

## 参考
- [バックエンドのモジュール接続仕様 · peinan/coeic Wiki](https://github.com/peinan/coeic/wiki/%E3%83%90%E3%83%83%E3%82%AF%E3%82%A8%E3%83%B3%E3%83%89%E3%81%AE%E3%83%A2%E3%82%B8%E3%83%A5%E3%83%BC%E3%83%AB%E6%8E%A5%E7%B6%9A%E4%BB%95%E6%A7%98)
