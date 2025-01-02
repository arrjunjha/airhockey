import cv2
import numpy as np
from utils.hand_detection import HandDetection
from utils.Ball import Ball
from utils.Paddle import Paddle
from utils.collision import collision
from utils.constants import WIDTH, HEIGHT, ball_radius, PADDLE_WIDTH, PADDLE_HEIGHT, WHITE, speed_increment

# Initialize video capture
vid = cv2.VideoCapture(0)
# Create an instance of HandDetection
hand_detection = HandDetection()
hand_detection.create_trackbars()



# Function to draw pieces in the main function
def draw_pieces(frame, ball, scoreCount, missCount):
    cv2.putText(frame, f"Score: {scoreCount}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f"Miss: {missCount}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    ball.draw(frame)

def main():
    # paddle = Paddle(WIDTH//2, HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT, WHITE)
    paddle1 = Paddle(50, 240, PADDLE_WIDTH, PADDLE_HEIGHT, (255, 0, 0))  
    paddle2 = Paddle(590, 240, PADDLE_WIDTH, PADDLE_HEIGHT, (0, 255, 0))
    ball = Ball(WIDTH//2, HEIGHT//2, ball_radius, 5, WHITE)
    # Initialise Score Variables
    scoreCount = 0
    missCount = 0
    while vid.isOpened():
        ret, frame = vid.read()
        if not ret:
            break

        mask = hand_detection.create_mask(frame)
        clean_mask = hand_detection.clean_image(mask)
        thresh_img = hand_detection.threshold(clean_mask)
        contours = hand_detection.find_contours(thresh_img)
        largest_contours = hand_detection.two_largest_contours(contours)

        centroids = []
        for contour in largest_contours:
            cx, cy = hand_detection.centroid(contour)
            centroids.append((cx, cy))
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

        # Assign centroids to paddles
        if len(centroids) == 1:
            paddle1.move(paddle1.x, centroids[0][1])
        elif len(centroids) == 2:
            centroids = sorted(centroids, key=lambda c: c[0])  # Sort by x-coordinate
            paddle1.move(paddle1.x, centroids[0][1])
            paddle2.move(paddle2.x, centroids[1][1])

        # Draw paddles
        paddle1.draw(frame)
        paddle2.draw(frame)
        # paddle.move(frame, centroid_x)
        # ball.move()
        draw_pieces(frame, ball, scoreCount, missCount)
        # # handle collision function here
        # collision(ball, paddle)
        # # Implement Score Functionality
        # if (ball.y > HEIGHT):
        #     missCount += 1
        #     if (missCount >= 3):
        #         scoreCount = 0
        #         missCount = 0
        #     ball.reset()
        # if (
        #     ball.y + ball.radius >= paddle.y - paddle.height and
        #     ball.x + ball.radius >= paddle.x - paddle.width // 2 and
        #     ball.x - ball.radius <= paddle.x + paddle.width // 2
        # ):
        #     scoreCount += 1

        frame = cv2.flip(frame, 1)
        cv2.imshow('Hand Gesture Slider', frame)

        key = cv2.waitKey(10)

        if key == ord('q'):
            break

    # Release the video capture and close all OpenCV windows
    vid.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
