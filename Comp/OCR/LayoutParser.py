

import layoutparser as lp
import cv2
import sys

# 画像読み込み
if len(sys.argv) < 2:
    print("Usage: python xxxx.py <image_file>")
    sys.exit(1)
image_path = sys.argv[1]
image = cv2.imread(image_path)

# PubLayNet の Table 検出モデル
# model = lp.Detectron2LayoutModel(
#     config_path='lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config',
#     label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"},
#     extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.5]
# )
# PaddleDetection の表検出モデル
model = lp.PaddleDetectionLayoutModel(
    config_path="lp://PubLayNet/ppyolov2_r50vd_dcn_365e_publaynet/config",
    threshold=0.5,
    label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"}
)

# レイアウト検出
layout = model.detect(image)

# Table のみ抽出
tables = layout.filter_by(type="Table")

print(tables)
