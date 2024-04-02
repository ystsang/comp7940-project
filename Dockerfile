FROM python
WORKDIR /APP
COPY . /APP
RUN pip install update
RUN pip install -r requirements.txt

ENV ACCESS_TOKEN=6878688568:AAHwAYRGrVSJ8eIfq6ULTVe5zyPLN72KvQ8
ENV BASICURL=https://chatgpt.hkbu.edu.hk/general/rest
ENV MODELNAME = gpt-4-turbo
ENV APIVERSION = 2024-02-15-preview
ENV GPT_ACCESS_TOKEN = 0f6806ea-482c-462d-8a9c-f24ae0f4f695

CMD python chatbot.py