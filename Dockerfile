FROM LEGEND-AI/LEGENDBOT:slim-buster

#clonning repo 

RUN git clone https://github.com/LEGEND-AI/LEGENDUSERBOT.git /root/Legendbot

#working directory 
WORKDIR /root/Legendbot

# Install requirements
RUN pip3 install --no-cache-dir -r requirements.txt


ENV PATH="/home/Legendbot/bin:$PATH"

CMD ["python3","-m","Legendbot"]
