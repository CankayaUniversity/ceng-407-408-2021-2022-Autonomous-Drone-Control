#what to do according to the location of the obstacle
import cv2

cap = cv2.VideoCapture(2)  # getting video from webcam
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

cap.set(3, frame_width)
cap.set(4, frame_width)
vertical_line_start = (frame_width // 2, 0)
vertical_line_end = (frame_width // 2, frame_height)
color = (97, 3, 24)
thickness = 2
horizontal_line_start = (0, frame_height // 2)
horizontal_line_end = (frame_width, frame_height // 2)
while 1:
    ret, img = cap.read()
    # cv2.line(image1, vertical_line_start, vertical_line_end, color, thickness)
    # cv2.line(image1, horizontal_line_start, horizontal_line_end, color, thickness)

    for i in range(0, frame_width, 5):
        cv2.circle(img, (frame_width // 2, i), radius=0, color=color, thickness=1)
        cv2.circle(img, (i, frame_height // 2), radius=0, color=color, thickness=1)
    start_point = (100, 100)
    # y=h/2 -pixelh
    # x=pixelw-w/2

    end_point = (350, 350)

    cv2.rectangle(img, start_point, end_point, (0, 255, 0), thickness)
    # print("A", start_point)
    # print("B", end_point[0], start_point[1])
    # print("C", start_point[0], end_point[1])
    # print("D", end_point)
    # cv2.circle(image1, start_point, radius=0, color=(0, 0, 255), thickness=1)
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
        # sdkdef.manualControl(0,50,450,0)
    if (A[0] >= 0 and A[1] >= 0) and (B[0] >= 0 and B[1] >= 0) and (C[0] >= 0 and C[1] >= 0) and (
            D[0] >= 0 and D[1] >= 0):
        print("go left and down")

    if (A[0] >= 0 and A[1] <= 0) and (B[0] > 0 and B[1] < 0) and (C[0] > 0 and C[1] < 0) and (D[0] >= 0 and D[1] <= 0):
        print("go left and up")

    if (A[0] < 0 and A[1] < 0) and (B[0] < 0 and B[1] < 0) and (C[0] < 0 and C[1] < 0) and (D[0] < 0 and D[1] < 0):
        print("go right and up")
    # ------------------------------------------------------------------------------------------------------------------
    if (A[0] < 0 and A[1] > 0) and (B[0] < 0 and B[1] > 0) and (C[0] < 0 and C[1] < 0) and (D[0] < 0 and D[1] < 0):
        # right
        short_edge = abs(A[0] - B[0])
        M_long_edge = abs(A[1] - 0)
        J_long_edge = abs(C[1] - 0)

        if M_long_edge * short_edge > J_long_edge * short_edge:
            print("right and down")
        elif M_long_edge * short_edge < J_long_edge * short_edge:
            print("right and up")
        else:
            print("right")
    if (A[0] < 0 and A[1] > 0) and (B[0] > 0 and B[1] > 0) and (C[0] < 0 and C[1] > 0) and (D[0] > 0 and D[1] > 0):
        # down
        short_edge = abs(A[0] - B[0])
        M_long_edge = abs(A[1] - 0)
        J_long_edge = abs(C[1] - 0)

        if M_long_edge * short_edge > J_long_edge * short_edge:
            print("right and down")
        elif M_long_edge * short_edge < J_long_edge * short_edge:
            print("left and down")

        else:
            print("left")

    if (A[0] > 0 and A[1] > 0) and (B[0] > 0 and B[1] > 0) and (C[0] > 0 and C[1] < 0) and (D[0] > 0 and D[1] < 0):
        # left
        long_edge = abs(A[1] - C[1])
        M_short_edge = abs(A[0] - 0)
        J_short_edge = abs(B[0] - 0)

        if M_short_edge * long_edge < J_short_edge * long_edge:
            print("left and up")
        elif M_short_edge * long_edge > J_short_edge * long_edge:
            print("left and down")

        else:
            print("down")

    if (A[0] <= 0 and A[1] <= 0) and (B[0] >= 0 and B[1] <= 0) and (C[0] <= 0 and C[1] <= 0) and (
            D[0] >= 0 and D[1] <= 0):
        # yukarı
        long_edge = abs(A[1] - C[1])
        M_short_edge = abs(A[0] - 0)
        J_short_edge = abs(B[0] - 0)

        if M_short_edge * long_edge > J_short_edge * long_edge:
            print("right and up")
        elif M_short_edge * long_edge < J_short_edge * long_edge:
            print("left and up")

        else:
            print("up")
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
        elif O_edge_1 * O_edge_2 > ((M_edge_1 * M_edge_2) and (J_edge_1 * J_edge_2) and (K_edge_1 * K_edge_2)):
            print("left and down")
        elif J_edge_1 * J_edge_2 > ((O_edge_1 * O_edge_2) and (M_edge_1 * M_edge_2) and (K_edge_1 * K_edge_2)):
            print("right and up")
        elif K_edge_1 * K_edge_2 > ((M_edge_1 * M_edge_2) and (J_edge_1 * J_edge_2) and (O_edge_1 * O_edge_2)):
            print("left and up")
        elif M_edge_1 * M_edge_2 == (O_edge_1 * O_edge_2) > ((J_edge_1 * J_edge_2) and (K_edge_1 * K_edge_2)):
            print("downand right or left")
        elif M_edge_1 * M_edge_2 == (J_edge_1 * J_edge_2) > ((O_edge_1 * O_edge_2) and (K_edge_1 * K_edge_2)):
            print("right and up or down")
        elif K_edge_1 * K_edge_2 == (J_edge_1 * J_edge_2) > ((O_edge_1 * O_edge_2) and (M_edge_1 * M_edge_2)):
            print("up and right or left")
        elif K_edge_1 * K_edge_2 == (O_edge_1 * O_edge_2) > ((J_edge_1 * J_edge_2) and (M_edge_1 * M_edge_2)):
            print("left and down or up")
        else:
            print("right or down and/or down or up")

    cv2.namedWindow("Frame", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Frame", img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord('p'):
        cv2.waitKey(-1)  # wait until any key is pressed
cap.release()
cv2.destroyAllWindows()
