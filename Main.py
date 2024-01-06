import streamlit as st
from st_xatadb_connection import XataConnection
import requests

st.set_page_config(page_title='Xata Demo',layout='wide')
xata = st.connection('xata',type=XataConnection)
st.subheader('Gallery demo')
st.divider()
if "Images" not in st.session_state or st.session_state.Images is None:
    st.session_state["Images"] = xata.query("Images",{"page":{ "size": 6}, "sort": {"xata.createdAt": "desc"}})

def update_images():
    st.session_state.Images = xata.query("Images",{"page":{ "size": 6}, "sort": {"xata.createdAt": "desc"}})


def upload():
    file = st.file_uploader("Upload file", type=["jpg", "png"])
    url = st.text_input("Or provide a URL")
    caption = st.text_area("Caption")

    if st.button("Upload",disabled=True):

        data = requests.get(url,timeout=5,stream=True).content

        if url != "":
            try:
                img = xata.insert("Images",{ "caption": caption})
            except Exception as e:
                st.write("Failed to create image")
                st.error(e)
            try:
                xata.upload_file("Images", img["id"], "image",data, "image/jpeg")
                st.success("Uploaded")
                update_images()
                st.rerun()
            except Exception as e:
                xata.delete("Images", img["id"])
                st.write("Failed to upload image")
                st.error(e)

        if file is not None:
            try:
                img = xata.insert("Images",{ "caption": caption})
            except Exception as e:
                st.write("Failed to create image")
                st.error(e)
            try:
                xata.upload_file("Images", img["id"], "image", file.read(), file.type)
                st.success("Uploaded")
                update_images()
                st.rerun()
            except Exception as e:
                xata.delete("Images", img["id"])
                st.write("Failed to upload image")
                st.error(e)

def show_images( images):

    if images is not None:
        cols = st.columns(3)
        if len(images) > 0:
            cols[0].image(images[0]["image"]["url"], width=200, caption=images[0]["caption"],use_column_width=True)
        if len(images) > 1:
            cols[1].image(images[1]["image"]["url"], width=200, caption=images[1]["caption"],use_column_width=True)
        if len(images) > 2:
            cols[2].image(images[2]["image"]["url"], width=200, caption=images[2]["caption"],use_column_width=True)

        cols2 = st.columns(3)
        if len(images) > 3:
            cols2[0].image(images[3]["image"]["url"], width=200, caption=images[3]["caption"],use_column_width=True)
        if len(images) > 4:
            cols2[1].image(images[4]["image"]["url"], width=200, caption=images[4]["caption"],use_column_width=True)
        if len(images) > 5:
            cols2[2].image(images[5]["image"]["url"], width=200, caption=images[5]["caption"],use_column_width=True)

show_images(st.session_state.Images["records"])
colss = st.columns([0.3,0.2,0.2,0.3])
if colss[1].button("Previous"):
    st.session_state.Images = xata.prev_page("Images",st.session_state.Images,pagesize=6)
    st.rerun()
if colss[2].button("Next"):
    st.session_state.Images = xata.next_page("Images",st.session_state.Images,pagesize=6)
    st.rerun()
st.write()

if st.toggle("Upload Image"):
    upload()




st.divider()
st.caption("Made with ❤️ by Sergio Lopez Martinez")
st.caption("Powered by Xata")
