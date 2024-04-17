import cv2

def calculate_difference(frame1, frame2):
  """Calculates the mean absolute difference between two RGB frames."""
  if frame1.shape != frame2.shape:
    raise ValueError("Frames must have the same dimensions")
  M, N = frame1.shape[:2]  # Extract only height and width
  sum_diff = 0
  for i in range(M):
    for j in range(N):
      # Access individual color channels (B, G, R)
      diff_b = abs(frame1[i, j][0] - frame2[i, j][0])
      diff_g = abs(frame1[i, j][1] - frame2[i, j][1])
      diff_r = abs(frame1[i, j][2] - frame2[i, j][2])
      sum_diff += diff_b + diff_g + diff_r
  return sum_diff / (M * N * 3)  # Divide by total channels (RGB)

def main():
  # Replace 'video.mp4' with your video filename
  cap = cv2.VideoCapture('test.MOV')

  if not cap.isOpened():
    print("Error opening video!")
    return

  # Read the first frame for initialization
  ret, prev_frame = cap.read()

  while True:
    ret, frame = cap.read()
    if not ret:
      break

    # Calculate difference and print result
    diff = calculate_difference(prev_frame, frame)
    print(diff)

    prev_frame = frame.copy()  # Update previous frame for next iteration

  cap.release()
  cv2.destroyAllWindows()

if __name__ == "__main__":
  main()
