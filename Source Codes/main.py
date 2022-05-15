#After the model detects the object, it draws around the detected object and moves according to its location.
import cv2
import numpy as np
import time
import psdk

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (416, 416))

    frame_width = frame.shape[1]
    frame_height = frame.shape[0]

    frame_blob = cv2.dnn.blobFromImage(frame, 1 / 255, (416, 416), swapRB=True, crop=False)

    labels = ["trainedobjectnames"]

    colors = ["0,0,255", "0,0,255", "255,0,0", "255,255,0", "0,255,0"]
    colors = [np.array(color.split(",")).astype("int") for color in colors]
    colors = np.array(colors)
    colors = np.tile(colors, (18, 1))

    model = cv2.dnn.readNetFromDarknet(r"yolov4-obj.cfg", r"yolov4-obj_last.weights")

    layers = model.getLayerNames()

    output_layer = [layers[i - 1] for i in model.getUnconnectedOutLayers()]

    model.setInput(frame_blob)

    detection_layers = model.forward(output_layer)

    ids_list = []
    boxes_list = []
    confidences_list = []

    for detection_layer in detection_layers:
        for object_detection in detection_layer:

            scores = object_detection[5:]
            predicted_id = np.argmax(scores)
            confidence = scores[predicted_id]

            if confidence > 0.20:
                label = labels[predicted_id]
                bounding_box = object_detection[0:4] * np.array([frame_width, frame_height, frame_width, frame_height])
                (box_center_x, box_center_y, box_width, box_height) = bounding_box.astype("int")

                start_x = int(box_center_x - (box_width / 2))
                start_y = int(box_center_y - (box_height / 2))

                ids_list.append(predicted_id)
                confidences_list.append(float(confidence))
                boxes_list.append([start_x, start_y, int(box_width), int(box_height)])

    max_ids = cv2.dnn.NMSBoxes(boxes_list, confidences_list, 0.5, 0.4)

    for max_id in max_ids:
        max_class_id = max_id[0]
        box = boxes_list[max_class_id]

        start_x = box[0]
        start_y = box[1]
        box_width = box[2]
        box_height = box[3]

        predicted_id = ids_list[max_class_id]
        label = labels[predicted_id]
        confidence = confidences_list[max_class_id]

        end_x = start_x + box_width
        end_y = start_y + box_height

        box_color = colors[predicted_id]
        box_color = [int(each) for each in box_color]

        label = "{}: {:.2f}%".format(label, confidence * 100)

        start_point = (start_x, start_y)
        # y=h/2 -pixelh
        # x=pixelw-w/2

        end_point = (end_x, end_y)

        # print("predicted object {}".format(label))

        Ax = start_point[0]
        Bx = end_point[0]
        Cx = start_point[0]
        Dx = end_point[0]
        Ay = start_point[1]
        By = start_point[1]
        Cy = end_point[1]
        Dy = end_point[1]
        A = Ax - frame_width // 2, frame_height // 2 - Ay
        B = Bx - frame_width // 2, frame_height // 2 - By
        C = Cx - frame_width // 2, frame_height // 2 - Cy
        D = Dx - frame_width // 2, frame_height // 2 - Dy
        print(A, B, C, D)

        short_edge = 0
        if (A[0] <= 0 and A[1] >= 0) and (B[0] <= 0 and B[1] >= 0) and (C[0] <= 0 and C[1] >= 0) and (
                D[0] <= 0 and D[1] >= 0):
            print("go right and down")
            psdk.manualConrtol(0, 500, 250)
            # sdkdef.manualControl(0,50,450,0)
        if (A[0] >= 0 and A[1] >= 0) and (B[0] >= 0 and B[1] >= 0) and (C[0] >= 0 and C[1] >= 0) and (
                D[0] >= 0 and D[1] >= 0):
            print("go left and down")
            psdk.manualConrtol(0, -500, 250)

        if (A[0] >= 0 and A[1] <= 0) and (B[0] > 0 and B[1] < 0) and (C[0] > 0 and C[1] < 0) and (
                D[0] >= 0 and D[1] <= 0):
            print("go left and up")
            psdk.manualConrtol(0, -500, 750)

        if (A[0] < 0 and A[1] < 0) and (B[0] < 0 and B[1] < 0) and (C[0] < 0 and C[1] < 0) and (D[0] < 0 and D[1] < 0):
            print("go right and up")
            psdk.manualConrtol(0, 500, 750)
        # ------------------------------------------------------------------------------------------------------------------
        if (A[0] < 0 and A[1] > 0) and (B[0] < 0 and B[1] > 0) and (C[0] < 0 and C[1] < 0) and (D[0] < 0 and D[1] < 0):
            # right
            short_edge = abs(A[0] - B[0])
            M_long_edge = abs(A[1] - 0)
            J_long_edge = abs(C[1] - 0)

            if M_long_edge * short_edge > J_long_edge * short_edge:
                print("right and down")
                psdk.manualConrtol(0, 500, 250)
            elif M_long_edge * short_edge < J_long_edge * short_edge:
                print("right and up")
                psdk.manualConrtol(0, 500, 750)
            else:
                print("right")
                psdk.manualConrtol(0, 500, 0)
        if (A[0] < 0 and A[1] > 0) and (B[0] > 0 and B[1] > 0) and (C[0] < 0 and C[1] > 0) and (D[0] > 0 and D[1] > 0):
            # down
            short_edge = abs(A[0] - B[0])
            M_long_edge = abs(A[1] - 0)
            J_long_edge = abs(C[1] - 0)

            if M_long_edge * short_edge > J_long_edge * short_edge:
                print("right and down")
                psdk.manualConrtol(0, -500, 250)
            elif M_long_edge * short_edge < J_long_edge * short_edge:
                print("left and down")
                psdk.manualConrtol(0, 500, 250)

            else:
                print("left")
                psdk.manualConrtol(0, -500, 0)

        if (A[0] > 0 and A[1] > 0) and (B[0] > 0 and B[1] > 0) and (C[0] > 0 and C[1] < 0) and (D[0] > 0 and D[1] < 0):
            # left
            long_edge = abs(A[1] - C[1])
            M_short_edge = abs(A[0] - 0)
            J_short_edge = abs(B[0] - 0)

            if M_short_edge * long_edge < J_short_edge * long_edge:
                print("left and up")
                psdk.manualConrtol(0, -500, 750)
            elif M_short_edge * long_edge > J_short_edge * long_edge:
                print("left and down")
                psdk.manualConrtol(0, -500, 250)

            else:
                print("down")
                psdk.manualConrtol(0, 0, 250)

        if (A[0] <= 0 and A[1] <= 0) and (B[0] >= 0 and B[1] <= 0) and (C[0] <= 0 and C[1] <= 0) and (
                D[0] >= 0 and D[1] <= 0):
            # up
            long_edge = abs(A[1] - C[1])
            M_short_edge = abs(A[0] - 0)
            J_short_edge = abs(B[0] - 0)

            if M_short_edge * long_edge > J_short_edge * long_edge:
                print("right and up")
                psdk.manualConrtol(0, 500, 750)
            elif M_short_edge * long_edge < J_short_edge * long_edge:
                print("left and up")
                psdk.manualConrtol(0, -500, 750)

            else:
                print("up")
                psdk.manualConrtol(0, 0, 250)
        # -----------------------------------------------------------------------------------------
        if (A[0] <= 0 and A[1] >= 0) and (B[0] >= 0 and B[1] >= 0) and (C[0] <= 0 and C[1] <= 0) and (
                D[0] >= 0 and D[1] <= 0):
            M_edge_1 = abs(A[0] - 0)
            M_edge_2 = abs(A[1] - 0)

            O_edge_1 = abs(C[0] - 0)
            O_edge_2 = abs(C[1] - 0)

            J_edge_1 = abs(B[0] - 0)
            J_edge_2 = abs(B[1] - 0)

            K_edge_1 = abs(D[0] - 0)
            K_edge_2 = abs(D[1] - 0)

            if M_edge_1 * M_edge_2 > ((O_edge_1 * O_edge_2) and (J_edge_1 * J_edge_2) and (K_edge_1 * K_edge_2)):
                print("right and down")
                psdk.manualConrtol(0, 500, 250)
            elif O_edge_1 * O_edge_2 > ((M_edge_1 * M_edge_2) and (J_edge_1 * J_edge_2) and (K_edge_1 * K_edge_2)):
                print("left and down")
                psdk.manualConrtol(0, -500, 250)
            elif J_edge_1 * J_edge_2 > ((O_edge_1 * O_edge_2) and (M_edge_1 * M_edge_2) and (K_edge_1 * K_edge_2)):
                print("right and up")
                psdk.manualConrtol(0, 500, 750)
            elif K_edge_1 * K_edge_2 > ((M_edge_1 * M_edge_2) and (J_edge_1 * J_edge_2) and (O_edge_1 * O_edge_2)):
                print("left and up")
                psdk.manualConrtol(0, -500, 750)
            elif M_edge_1 * M_edge_2 == (O_edge_1 * O_edge_2) > ((J_edge_1 * J_edge_2) and (K_edge_1 * K_edge_2)):
                print("downand right or left")
                psdk.manualConrtol(0, 500, 250)
            elif M_edge_1 * M_edge_2 == (J_edge_1 * J_edge_2) > ((O_edge_1 * O_edge_2) and (K_edge_1 * K_edge_2)):
                print("right and up or down")
                psdk.manualConrtol(0, 500, 750)
            elif K_edge_1 * K_edge_2 == (J_edge_1 * J_edge_2) > ((O_edge_1 * O_edge_2) and (M_edge_1 * M_edge_2)):
                print("up and right or left")
                psdk.manualConrtol(0, 500, 750)
            elif K_edge_1 * K_edge_2 == (O_edge_1 * O_edge_2) > ((J_edge_1 * J_edge_2) and (M_edge_1 * M_edge_2)):
                print("left and down or up")
                psdk.manualConrtol(0, -500, 750)
            else:
                print("right or down and/or down or up")
                psdk.manualConrtol(0, 500, 750)
        psdk.manualConrtol(500, 0, 0)
        # cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), box_color, 2)
        # cv2.rectangle(frame, (start_x - 1, start_y), (end_x + 1, start_y - 30), box_color, -1)
        # cv2.putText(frame, label, (start_x, start_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    if cv2.waitKey(1) & ord("q") == 27:
        break

    cv2.imshow("Detector", frame)
