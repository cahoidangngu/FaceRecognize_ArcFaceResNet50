import streamlit as st
from PIL import Image
import numpy as np
from app import App

if __name__ == "__main__":
    st.sidebar.markdown("# Face Registration")
    st.markdown("# Face Recognition App")
    app = App()
  

    img_file_buffer = st.camera_input("Take a photo to register a new user")

    user_type = st.selectbox("Select User Type", ["New User", "Registered User"])
    registered_users = app.get_all_people()
    selected_user = ""

    if user_type == "New User":
        new_user_name = st.text_input("Enter New Name:")
    elif user_type == "Registered User":
        selected_user = st.selectbox(
            "Select registered user",
            options=registered_users,
            format_func=lambda x: f'{x["name"]} ({x["id"]})',
        )
        faces = app.get_faces_by_person_id(str(selected_user["id"]))
        row_size = 3
        grid = st.columns(row_size)
        col = 0
        for face in faces:
            with grid[col]:
                st.image(face["image"])
        col = (col + 1) % row_size
    submit_button = st.button("Submit")

    if submit_button:
        if img_file_buffer is not None:
            # To read the image file buffer as a PIL Image:

            img_buffer = Image.open(img_file_buffer)

            # To convert PIL Image to a numpy array:
            img_array = np.array(img_buffer)

            # Display the image with the selected user's name as the caption
            if user_type == "New User":
                st.write("Registering new user...")
                app.add_new_person(name=new_user_name, image=img_array)
                st.write("New user registered!")
                st.image(img_array, caption=new_user_name)
            elif user_type == "Registered User":
                pid = str(selected_user["id"])
                st.write(pid)
                app.add_new_face(person_id=pid, image=img_array)
                st.image(img_array, caption=selected_user)
