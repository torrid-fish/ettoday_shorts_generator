from script import script_generator
from audio import human_voice_generator, effect_generator, bgm_generator

def main(length: int, text: str, imgs: list[str], imgsDescription: list[str], gerne: str, dest: str) -> bool:
    """
    ## Args
    - length: The length of the video.
    - text: The text of the news.
    - imgs: The list of string represents path to those images that are used in the news.
    - imgsDescription: The list of string that describe the images.
    - gerne: What type of the news it is.
    - dest: The destination path of the output videos.
    ## Return
    - (bool): Whether the video is successfully generated.
    """
    try:
        # Generate scipt to read
        sentences = script_generator(text, length, imgsDescription)
        title = sentences[0]["title"]
        titleKeywords = sentences[0]["keyword"]
        intro = sentences[0]["outline"][1]
        outro = sentences[0]["outline"][0] 

        # Generate audio
        data = []
        totalLength = 0
        ## Generate title audio
        audio, length, timeStampes = human_voice_generator(title, titleKeywords, gerne, addEffect=False, reader="F1")
        data.append({
            "text": title,
            "length": length,
            "keywords": titleKeywords,
            "timeStamps": timeStampes,
            "image": None
        })
        totalLength += length
        ## Generate intro audio
        _audio, length, timeStampes = human_voice_generator(intro, []) # No keywords
        audio += _audio
        data.append({
            "text": intro,
            "length": length,
            "keywords": None,
            "timeStamps": None,
            "image": None
        })
        totalLength += length
        ## Generate content audio
        for setence in sentences[1:]:
            script = setence["script"]
            imageDescription = sentences["imageDescription"]
            keywords = setence["keywords"]
            _audio, length, timeStampes = human_voice_generator(script, keywords)
            audio += _audio
            data.append({
                "text": script,
                "length": length,
                "keywords": keywords,
                "timeStamps": timeStampes
                #"image": image,
            })
            totalLength += length
        ## Generate outro audio
        _audio, length, timeStampes = human_voice_generator(outro, []) # No keywords
        audio += _audio
        data.append({
            "text": intro,
            "length": length,
            "keywords": None,
            "timeStamps": None,
            "image": None
        })
        totalLength += length
        
        assert len(audio) == totalLength, "Error: Audio length didn't match."
        bgm = bgm_generator(gerne, length)

        audio.overlay(bgm, position=0)

        # Start producing video
        '''
        - audio: Final audio data
        - totalLength: The length of this audio data
        - data: Data of each sentence, which contains 
            - "text"
            - "length"
            - "keywords"
            - "timeStamps"
            - "images"
        '''
        # Simple test
        audio.export("./result.wav", format="wav")
        print(totalLength)
        for d in data:
            print(d)

        return True
    except ...:
        return False

length = 10
text = "在清華大學的梅竹黑客松，有超過100位學生參加。許多人都非常期待這次比賽的結果。"
imgsDescription = ["學生在電腦前認真編寫程式碼"]
gerne="科技"

main(length=length, text=text, imgsDescription=imgsDescription, gerne=gerne, imgs=[], dest="")
