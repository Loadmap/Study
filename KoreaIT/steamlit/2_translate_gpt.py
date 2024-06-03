import streamlit as st
import openai

openai.api_key = ''

example = {
    '한국어' : ['오늘 날씨가 어떤가요?', '딥러닝 기반의 AI 기술이 인기를 끌고 있다.'],
    '영어' : ['How is the weather today?', 'AI technology based on deep learning is gaining popularity.'],
    '일본어' : ['今日の天気はどうですか？', 'ディープラーニング基盤のAI技術が人気を集めている。']
}

def translate_text_chatgpt(text, src_lang, trg_lang) :

    def build_fewshot(src_lang, trg_lang) :
        src_examples = example[src_lang]
        trg_examples = example[trg_lang]

        fewshot_message = []

        for src_text, trg_text in zip(src_examples, trg_examples) :
            fewshot_message.append({'role' : 'user', 'content' : src_text})
            fewshot_message.append({'role': 'assistant', 'content': trg_text})

        return fewshot_message

    system_instruction = f'assistant 는 번역 앱으로 동작한다. {src_lang}를 {trg_lang}으로 적절하게 번역하고 번역된 텍스트만 출력한다.'
    fewshot_messages = build_fewshot(src_lang = src_lang, trg_lang = trg_lang)

    message = [{'role' : 'system', 'content' : system_instruction}, *fewshot_messages, {'role' : 'user', 'content' : text}]
    # print(message)

    response = openai.chat.completions.create(
        model = 'gpt-3.5-turbo', messages = message

    )
    # print(response)
    # print(response.choices[0].message.content)
    return response.choices[0].message.content

st.title('초간단 번역 서비스앱')
text = st.text_area('번역할 내용을 입력하세요 : ', '')
src_lang = st.selectbox('번역할 언어를 선택하세요.',['영어', '일본어', '한국어'])
trg_lang = st.selectbox('번역된 언어를 선택하세요.',['영어', '일본어', '한국어'])

if st.button('번역하기') :
    translated_text = translate_text_chatgpt(text, src_lang, trg_lang)
    st.success(translated_text)