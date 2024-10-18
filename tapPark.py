import cv2
import pytesseract
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import PhotoImage

# Create the main window
root = tk.Tk()
root.title("TapPARK | System")
root.geometry("1200x600")

# Load the logo image
logo = PhotoImage(file="TapPARK.png")
root.iconphoto(False, logo)

# Function to update canvas size on window resize
def resize_canvas(event, canvas):
    canvas.config(width=event.width, height=event.height)


# Make the window responsive
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)

# Left large container
left_frame = tk.Frame(root, bg="lightgray", width=400, height=300)
left_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)

# Make left_frame rows and columns responsive
left_frame.grid_rowconfigure(0, weight=1)
left_frame.grid_rowconfigure(1, weight=1)
left_frame.grid_rowconfigure(2, weight=1)
left_frame.grid_columnconfigure(0, weight=1)
left_frame.grid_columnconfigure(1, weight=1)
left_frame.grid_columnconfigure(2, weight=1)

# Right top container
right_top_frame = tk.Frame(root, bg="gray", width=200, height=150)
right_top_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

# Right bottom container
right_bottom_frame = tk.Frame(root, bg="darkgray", width=200, height=150)
right_bottom_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=10)

# Bottom container
bottom_frame = tk.Frame(root, width=800, height=50)
bottom_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

# Make the frames responsive
root.grid_rowconfigure(0, weight=3)  
root.grid_rowconfigure(1, weight=3)  
root.grid_rowconfigure(2, weight=1)  

root.grid_columnconfigure(0, weight=2)  
root.grid_columnconfigure(1, weight=1) 



# Initialize
# current floor
current_floor = 1
buttons = {}
Plate_number = False
# Parking slot data with two values for each spot (A1, 01; A1, 02; A1, 03)
parking_slots = {
    1: {
        'A1, 01': {'occupied': False},
        'A1, 02': {'occupied': False},
        'A1, 03': {'occupied': False},
        'A2, 01': {'occupied': False},
        'A2, 02': {'occupied': False},
        'A2, 03': {'occupied': False},
        'A3, 01': {'occupied': False},
        'A3, 02': {'occupied': False},
        'A3, 03': {'occupied': False},
        'B1, 01': {'occupied': False},
        'B1, 02': {'occupied': False},
        'B1, 03': {'occupied': False},
        'B2, 01': {'occupied': False},
        'B2, 02': {'occupied': False},
        'B2, 03': {'occupied': False},
        'B3, 01': {'occupied': False},
        'B3, 02': {'occupied': False},
        'B3, 03': {'occupied': False},
        'C1, 01': {'occupied': False},
        'C1, 02': {'occupied': False},
        'C1, 03': {'occupied': False},
        'C2, 01': {'occupied': False},
        'C2, 02': {'occupied': False},
        'C2, 03': {'occupied': False},
        'C3, 01': {'occupied': False},
        'C3, 02': {'occupied': False},
        'C3, 03': {'occupied': False}
    },
    2: {
        'A1, 01': {'occupied': False},
        'A1, 02': {'occupied': False},
        'A1, 03': {'occupied': False},
        'A2, 01': {'occupied': False},
        'A2, 02': {'occupied': False},
        'A2, 03': {'occupied': False},
        'A3, 01': {'occupied': False},
        'A3, 02': {'occupied': False},
        'A3, 03': {'occupied': False},
        'B1, 01': {'occupied': False},
        'B1, 02': {'occupied': False},
        'B1, 03': {'occupied': False},
        'B2, 01': {'occupied': False},
        'B2, 02': {'occupied': False},
        'B2, 03': {'occupied': False},
        'B3, 01': {'occupied': False},
        'B3, 02': {'occupied': False},
        'B3, 03': {'occupied': False},
        'C1, 01': {'occupied': False},
        'C1, 02': {'occupied': False},
        'C1, 03': {'occupied': False},
        'C2, 01': {'occupied': False},
        'C2, 02': {'occupied': False},
        'C2, 03': {'occupied': False},
        'C3, 01': {'occupied': False},
        'C3, 02': {'occupied': False},
        'C3, 03': {'occupied': False}
    },
    3: {
        'A1, 01': {'occupied': False},
        'A1, 02': {'occupied': False},
        'A1, 03': {'occupied': False},
        'A2, 01': {'occupied': False},
        'A2, 02': {'occupied': False},
        'A2, 03': {'occupied': False},
        'A3, 01': {'occupied': False},
        'A3, 02': {'occupied': False},
        'A3, 03': {'occupied': False},
        'B1, 01': {'occupied': False},
        'B1, 02': {'occupied': False},
        'B1, 03': {'occupied': False},
        'B2, 01': {'occupied': False},
        'B2, 02': {'occupied': False},
        'B2, 03': {'occupied': False},
        'B3, 01': {'occupied': False},
        'B3, 02': {'occupied': False},
        'B3, 03': {'occupied': False},
        'C1, 01': {'occupied': False},
        'C1, 02': {'occupied': False},
        'C1, 03': {'occupied': False},
        'C2, 01': {'occupied': False},
        'C2, 02': {'occupied': False},
        'C2, 03': {'occupied': False},
        'C3, 01': {'occupied': False},
        'C3, 02': {'occupied': False},
        'C3, 03': {'occupied': False}
    }
}




# This section is the function code
# Load the car image and resize it to fit the button's proportions
car_image = Image.open("car.png")
car_image = car_image.resize((70, 40), Image.LANCZOS)  # Adjust the size to fit within the button
car_photo = ImageTk.PhotoImage(car_image)

# Function to update the slot's status (green for free, red for occupied)
def update_slot(slot_id, canvas):
    canvas.delete("all")
    if parking_slots[current_floor][slot_id]['occupied']:
        canvas.create_image(50, 22, image=car_photo)
        canvas.config(bg="red")
    else:
        canvas.create_text(50, 25, text=f"L{current_floor}, {slot_id}", fill="black")
        canvas.config(bg="green")

# Function to handle click on a slot
def on_slot_click(slot_id, canvas):
    
    if parking_slots[current_floor][slot_id]['occupied']:
        leave_ask = messagebox.askyesno("Leave Parking", f"Do you want to leave slot L{current_floor}{slot_id}?")
        if leave_ask:
            parking_slots[current_floor][slot_id]['occupied'] = False
            update_slot(slot_id, canvas)
    else:
        if Plate_number == True:
            park_ask = messagebox.askyesno("Park Here", f"Do you want to park in slot L{current_floor}{slot_id}?")
            if park_ask:
                parking_slots[current_floor][slot_id]['occupied'] = True
                plate_label2.config(text=f"L{current_floor}{slot_id}")
                make_if_false()
                update_slot(slot_id, canvas)
        else:
            leave_ask = messagebox.showinfo("Notice", "Don't have a plate number")

def make_if_false():
    global Plate_number
    Plate_number = False

# Function to update the video feed
def update_video_feed():
    ret, frame = cap.read()
    if ret:
        # Convert the frame to RGB format
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert the frame to a PIL image
        pil_image = Image.fromarray(rgb_frame)
        
        # Convert the PIL image to an ImageTk image
        imgtk = ImageTk.PhotoImage(image=pil_image)
        
        # Update the video label with the new frame
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
        
        # Detect license plates in the frame
        detect_license_plate(frame)
    
    # Schedule the next update
    video_label.after(10, update_video_feed)

# Function to detect license plates in a frame
def detect_license_plate(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    plates = plate_cascade.detectMultiScale(gray, 1.1, 10)
    
    
    for (x, y, w, h) in plates:
        plate = frame[y:y+h, x:x+w]
        plate_text = pytesseract.image_to_string(plate, config='--psm 8')
        
        if plate_text.strip():
            global Plate_number
            Plate_number = True
            plate_label.config(text=f"Plate Number: {plate_text.strip()}")
            # Draw a rectangle around the detected plate
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Convert the frame to RGB format for display
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_frame)
    imgtk = ImageTk.PhotoImage(image=pil_image)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)
    
# Function to start the camera feed
def start_camera():
    global cap
    cap = cv2.VideoCapture(0)
    
    # Set the width and height of the camera feed
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 620)  # Set width to 640 pixels
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 380)  # Set height to 480 pixels
    
    update_video_feed()



            
# Function to change the floor
def change_floor(floor):
    global current_floor
    current_floor = floor
    for slot_id, canvas in slot_canvases.items():
        update_slot(slot_id, canvas)

# Function to change the floor
def change_floor(floor):
    global current_floor
    current_floor = floor
    for slot_id, canvas in slot_canvases.items():
        update_slot(slot_id, canvas)
    # Update button colors
    for f, button in buttons.items():
        if f == floor:
            button.config(bg="green")
        else:
            button.config(bg="SystemButtonFace")
        
            
            
# This section is the main code
# Create the slot canvases and place them in a grid within left_frame
slot_canvases = {}
section_letters = ["A", "B", "C"]
slotno = 0
for i in range(3):
    for j in range(3): 
        section = section_letters[j]
        containerCanvas = tk.Canvas(left_frame, width=120, height=150, bg="lightgray",highlightthickness=0)
        containerCanvas.grid(row=i, column=j, padx=5, pady=5)
        for k in range(3): 
            slot_id = f'{section}{i+1}, 0{(k) + 1}'
            inner_slot_id = f'{slot_id}'
            slot_canvas = tk.Canvas(containerCanvas, width=100, height=40, bg="red")
            slot_canvas.place(x=10, y=0 + k*50)
            slot_canvas.bind("<Button-1>", lambda event, s=inner_slot_id, c=slot_canvas: on_slot_click(s, c))
            slot_canvases[inner_slot_id] = slot_canvas

            update_slot(inner_slot_id, slot_canvas)
            

# Create a label to display the video feed
video_label = tk.Label(right_top_frame)
video_label.pack(fill="both", expand=True)


# Create a label to display the detected plate number
plate_label2 = tk.Label(right_bottom_frame, text="", font=("Helvetica", 30), bg="darkgray", fg="white")
plate_label2.pack(pady=10) 

# Create a label to display the detected plate number
plate_label = tk.Label(right_bottom_frame, text="Plate Number: None", font=("Helvetica", 16), bg="darkgray", fg="white")
plate_label.pack() 
 
# Add a label with left-aligned text
left_aligned_label = tk.Label(bottom_frame, text=f"Levels", anchor="w", font=("Helvetica", 16))
left_aligned_label.pack(fill="both", padx=10, pady=0)

# Create floor buttons and place them inside the bottom container
floor_buttons = tk.Frame(bottom_frame)
floor_buttons.pack(pady=0, padx=10, anchor="w")

for floor in range(1, 4):
    button = tk.Button(floor_buttons, text=f"Floor {floor}", command=lambda f=floor: change_floor(f), font=("Helvetica", 12))
    button.pack(side=tk.LEFT, padx=5)
    buttons[floor] = button

#Default color for button
buttons[current_floor].config(bg="green")

# Load the pre-trained Haar Cascade for license plate detection
plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')

# Start the camera automatically
start_camera()

# Start the main 
root.mainloop()

# Release the video capture object when done
if 'cap' in globals():
    cap.release()
cv2.destroyAllWindows()