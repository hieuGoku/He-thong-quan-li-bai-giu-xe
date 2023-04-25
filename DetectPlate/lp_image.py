import cv2
import torch
import function.utils_rotate as utils_rotate
import function.helper as helper

# ap = argparse.ArgumentParser()
# ap.add_argument('-i', '--image', required=True, help='path to input image')
# args = ap.parse_args()

def detect_pl(img):
    yolo_LP_detect = torch.hub.load('yolov5', 'custom', path='E:\PBL5\License-Plate-Recognition\model\LP_detector.pt', force_reload=True, source='local')
    yolo_license_plate = torch.hub.load('yolov5', 'custom', path='E:\PBL5\License-Plate-Recognition\model\LP_ocr.pt', force_reload=True, source='local')
    yolo_license_plate.conf = 0.60

    # img = cv2.imread(img_path)
    plates = yolo_LP_detect(img, size=640)

    plates = yolo_LP_detect(img, size=640)
    list_plates = plates.pandas().xyxy[0].values.tolist()
    list_read_plates = set()
    if len(list_plates) == 0:
        lp = helper.read_plate(yolo_license_plate,img)
        if lp != "unknown":
            cv2.putText(img, lp, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            list_read_plates.add(lp)
    else:
        for plate in list_plates:
            flag = 0
            x = int(plate[0]) # xmin
            y = int(plate[1]) # ymin
            w = int(plate[2] - plate[0]) # xmax - xmin
            h = int(plate[3] - plate[1]) # ymax - ymin  
            crop_img = img[y:y+h, x:x+w]
            cv2.rectangle(img, (int(plate[0]),int(plate[1])), (int(plate[2]),int(plate[3])), color = (0,0,225), thickness = 2)
            cv2.imwrite("crop.jpg", crop_img)
            rc_image = cv2.imread("crop.jpg")
            lp = ""
            for cc in range(0,2):
                for ct in range(0,2):
                    lp = helper.read_plate(yolo_license_plate, utils_rotate.deskew(crop_img, cc, ct))
                    if lp != "unknown":
                        list_read_plates.add(lp)
                        cv2.putText(img, lp, (int(plate[0]), int(plate[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                        flag = 1
                        break
                if flag == 1:
                    break

    print(list_read_plates)


if __name__ == '__main__':
    # print(detect_pl('E:\\PBL5\\License-Plate-Recognition\\test_image\\bien_so.jpg'))
    img = cv2.imread("D:\\pexels-photo-1304626.jpg")
    print(detect_pl(img))