import streamlit as st
from PIL import Image
from io import BytesIO
import base64
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import anthropic

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# 設定模型
def model_output(my_upload1, my_upload2, my_upload3, my_upload4, my_upload5):
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

    image_paths = [my_upload1, my_upload2, my_upload3, my_upload4, my_upload5]
    image_captions = []
    for path in image_paths:
        image = Image.open(path).convert('RGB')
        inputs = processor(image, return_tensors="pt")
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)
        image_captions.append(caption)

    combined_prompt = "Based on the descriptions of the following 5 independent images, please generate a coherent story(don't mark number of images):\n\n"
    for i, caption in enumerate(image_captions, start=1):
        combined_prompt += f"Image{i} descriptions: {caption}\n\n"

    out = model.generate(**inputs)

    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key="YOUR_API_KEY",
    )
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": combined_prompt
                    }
                ]
            }
        ]
    )
    print(message.content[0].text)
    return message    



# 設定網頁
st.set_page_config(layout="wide", page_title="Image Background Remover")

st.write("## project image preview")
st.write(
    ""
)
default_image = [Image.open("./1.jpg"), Image.open("./2.jpg"), Image.open("./3.jpg"), Image.open("./4.jpg"), Image.open("./5.jpg")]


# Sidebar
st.sidebar.write("## Upload and start :gear:")
image_number_input = st.sidebar.number_input("Choose the number of images", min_value=3, max_value=10, value=3)

#current_image_number = st.sidebar.number_input("Choose the file order of images", min_value=1, max_value=10, value=1)

my_upload = [None] * image_number_input
for i in range(image_number_input):
    st.sidebar.write(f"Upload image {i + 1 }")
    my_upload.append(st.sidebar.file_uploader(f"Upload image {i + 1 }", type=["png", "jpg", "jpeg"]))

preview = []
preview = st.columns(image_number_input)

for i in range(image_number_input):
    if my_upload[i] is not None:
        preview[i].image(my_upload[i])
    else:
        preview[i].image(default_image[i%5])


# Main
st.write("## text and audio generation")
# Download the fixed image
show = []
for i in range(image_number_input):
    show.append(st.columns(image_number_input ))
    show[i][0].write(f"Image {i + 1 }")
    show[i][1].write(f"text {i + 1 }")
    show[i][2].audio("https://www.soundjay.com/button/beep-07.wav")
    if my_upload[i] is not None:
        show[i][0].image(my_upload[i])
    else:
        show[i][0].image(default_image[i%5])
    if my_upload[i] is not None:
        show[i][1].write("Uploaded Image")
    else:
        show[i][1].write("Default Image")

def image(upload , image_order):
    image = Image.open(upload)
    show[image_order][0].image(image)

    

#col1, col2, col3,col4,col5  = st.columns(5)

submit = st.sidebar.button("Submit")


message = None
if(submit): 
    message = model_output(my_upload[0], my_upload[1], my_upload[2], my_upload[3], my_upload[4])
    submit = False

st.write("## text generation")
st.audio("https://www.soundjay.com/button/beep-07.wav")
if message is not None:
    st.write(
        message.content[0].text
    )
else:
    st.write("Please upload images and click submit to generate text")
    st.write("\n\n\n\n\n")

st.video("https://www.soundjay.com/button/beep-07.wav")