import cv2

greyscale = True
threshold = 40 # 83 for car vid gooseball

def write_filtered_video(filtered_frames, output_filename):
  """Writes the filtered frames to a new video in MOV format."""
  # Get properties from the first frame (assuming all frames have same properties)
  first_frame = filtered_frames[0]
  height, width, channels = first_frame.shape
  

  fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Replace with 'XVID' for testing (won't work for MOV)

  out = cv2.VideoWriter(output_filename, fourcc, 25.0, (width, height))
  for frame in filtered_frames:
    out.write(frame)
    # cv2.imshow('frame', frame)   # displays finished vid
    c = cv2.waitKey(1)
    if c & 0xFF == ord('q'):
        break

  out.release()

def calculate_difference(frame1, frame2):
  """Calculates the mean absolute difference between two grayscale frames."""
  if frame1.shape != frame2.shape:
    raise ValueError("Frames must have the same dimensions")
  if greyscale:
    M, N = frame1.shape
  else:
    M, N = frame1.shape[:2]  # Extract only height and width

  sum_diff = 0
  # print(N,flush=True)
  # print(M,flush=True)


  for i in range(M):
    for j in range(N):
        if greyscale:
            sum_diff += abs(frame1[i, j] - frame2[i, j])
        else:
            # Access individual color channels (B, G, R)
            diff_b = abs(frame1[i, j][0] - frame2[i, j][0])
            diff_g = abs(frame1[i, j][1] - frame2[i, j][1])
            diff_r = abs(frame1[i, j][2] - frame2[i, j][2])
            sum_diff += diff_b + diff_g + diff_r

  if greyscale:          
    return sum_diff / (M * N)
  return sum_diff / (M * N * 3)  # Divide by total channels (RGB)


def main():
  # Replace 'video.mp4' with your video filename
  for i in range(8):
    filename = i + 1
    filename = str(filename) + '.mp4'
    print(filename)

    cap = cv2.VideoCapture('input/' + filename)

    if not cap.isOpened():
      print("Error opening video!")
      return

    # Read the first frame for initialization
    ret, prev_frame = cap.read()
    if greyscale:
      prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    filtered_frames = []  # List to store filtered frames

    while True:
      ret, frame = cap.read()
      if not ret:
        break

      current_frame = frame
      if greyscale:
          current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

      # Calculate difference and check against threshold
      diff = calculate_difference(prev_frame, current_frame)
      print(diff)
      if diff > threshold:  # Keep frame if difference is below threshold
        filtered_frames.append(frame.copy()) # store the RGB frame in the new vid list
        print("new frame")



      prev_frame = current_frame.copy()  # Update previous frame

    cap.release()
    cv2.destroyAllWindows()

    # Write filtered frames to a new video
    new_file_name = "finals/fr_" + filename

    write_filtered_video(filtered_frames, new_file_name)  # Change output filename


if __name__ == "__main__":
  main()



