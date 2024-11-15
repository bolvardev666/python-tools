import os.path

import cv2
import numpy as np


def mark_and_save_match(main_image_path, template_path, output_path="result.jpg", threshold=0.8):
    """
    在主图片中查找模板，标注最佳匹配位置并保存结果

    参数:
    main_image_path: 主图片路径
    template_path: 模板图片路径
    output_path: 输出图片路径
    threshold: 匹配阈值
    """
    # 读取图片
    main_image = cv2.imread(main_image_path)
    template = cv2.imread(template_path)

    if main_image is None or template is None:
        raise Exception("无法读取图片")

    # 获取模板尺寸
    h, w = template.shape[:2]

    # 执行模板匹配
    result = cv2.matchTemplate(main_image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        # 获取最佳匹配的左上角坐标
        top_left = max_loc
        # 计算右下角坐标
        bottom_right = (top_left[0] + w, top_left[1] + h)

        # 在图片上画矩形框
        cv2.rectangle(
            main_image,
            top_left,
            bottom_right,
            color=(0, 255, 0),  # 绿色
            thickness=1
        )

        # 计算中心点坐标
        center_x = top_left[0] + w // 2
        center_y = top_left[1] + h // 2

        # 画十字标记
        # cross_size = 20
        # cv2.line(
        #     main_image,
        #     (center_x - cross_size, center_y),
        #     (center_x + cross_size, center_y),
        #     color=(0, 0, 255),  # 红色
        #     thickness=2
        # )
        # cv2.line(
        #     main_image,
        #     (center_x, center_y - cross_size),
        #     (center_x, center_y + cross_size),
        #     color=(0, 0, 255),
        #     thickness=2
        # )

        # # 添加坐标文本
        # text = f"({center_x}, {center_y})"
        # cv2.putText(
        #     main_image,
        #     text,
        #     (center_x + 10, center_y - 10),
        #     cv2.FONT_HERSHEY_SIMPLEX,
        #     0.5,
        #     (255, 0, 0),  # 蓝色
        #     2
        # )
        #
        # # 添加匹配度信息
        # confidence_text = f"Confidence: {max_val:.2f}"
        # cv2.putText(
        #     main_image,
        #     confidence_text,
        #     (10, 30),
        #     cv2.FONT_HERSHEY_SIMPLEX,
        #     1,
        #     (0, 255, 0),
        #     2
        # )

        # 保存结果
        cv2.imwrite(output_path, main_image)

        print(f"匹配位置: 中心点({center_x}, {center_y})")
        print(f"匹配度: {max_val:.2f}")
        print(f"结果已保存至: {output_path}")

        return (center_x, center_y), max_val
    else:
        print(f"未找到匹配 (最大匹配度: {max_val:.2f})")
        return None, max_val


# 使用示例
if __name__ == "__main__":
    try:
        # 指定图片路径
        main_image = os.path.join(os.path.dirname(__file__),'img','微信截图_20241113142931.png')
        template = os.path.join(os.path.dirname(__file__),'flag', "template.png")
        output = "marked_result.jpg"

        # 执行匹配和标注
        position, confidence = mark_and_save_match(
            main_image,
            template,
            output,
            threshold=0.8
        )

    except Exception as e:
        print(f"错误: {str(e)}")

# Created/Modified files during execution:
# - marked_result.jpg